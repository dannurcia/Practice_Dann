""" Filtrado de documentos por entidades
    @dann_uc """


import json
import re
from deepdiff import DeepDiff

text_info_precio = []
questions_info_pago = ['dónde hago el depósito?', 'donde hago el depósito', 'cuando hago el depósito?',
                               'cuando hago el depósito', 'donde hago la transferencia', 'como hago la transferencia',
                               'como realizo la transferencia', 'quiero hacer la transferencia?']


def preprocess_message(msg):
    """
    Preprocesa el texto del mensaje para la obtención de una lista de tokens.

    :param msg: Texto del mensaje
    :return: preprocessed_msg - Mensaje preprocesado en formato de lista
    """
    # Adición de espacios para separar caracteres especiales al inicio del texto
    temp_msg = re.sub(r'^([^a-zA-Z\d])(.+)$', r'\1 \2', msg)
    # ---------------------------------------------------------------------------------------
    # Adición de espacios para separar caracteres especiales dentro del texto (EXCEPTO: [@_-°#$%&`~^*+<>|¬\{}=[]´])
    # Caso 1: caracteres especiales [,:'/] con significado al encontrarse entre números
    temp_msg = re.sub(r'''(\D)([,:'/])(\D)''', r'\1 \2 \3', temp_msg)
    temp_msg = re.sub(r'''(\d)([,:'/])(\D)''', r'\1 \2 \3', temp_msg)
    temp_msg = re.sub(r'''(\D)([,:'/])(\d)''', r'\1 \2 \3', temp_msg)
    temp_msg = re.sub(r' +', r' ', temp_msg)
    # Caso 2: caracteres especiales [;"¿?¡!()]
    temp_msg = re.sub(r'([;"¿?¡!()])', r' \1 ', temp_msg)
    temp_msg = re.sub(r' +', r' ', temp_msg)
    # Caso 3: punto
    temp_msg = re.sub(r'([a-zA-Z\d])(\.) ', r'\1 \2 ', temp_msg)
    temp_msg = re.sub(r' (\.)([a-zA-Z\d])', r' \1 \2', temp_msg)
    # temp_msg = re.sub(r'()(\.)()', r'\1 \2 \3', temp_msg)
    email_match = re.search(r'\w+(?:\.\w+)*@\w+(?:\.\w+)+', temp_msg)
    if email_match:
        l, u = email_match.span()
        pre = temp_msg[:l]
        post = temp_msg[u:]
        new_email = re.sub(r'\.', r'**.**', temp_msg[l:u])
        temp_msg = pre + new_email + post
    temp_msg = re.sub(r'([a-zA-Z])(\.)([a-zA-Z])', r'\1 \2 \3', temp_msg)
    if email_match:
        temp_msg = re.sub(r'\*\*\.\*\*', r'.', temp_msg)
    temp_msg = re.sub(r' +', r' ', temp_msg)
    # Caso 4: puntos suspensivos
    temp_msg = re.sub(r'\.{3,}', r' Puntos_suspensivoS ', temp_msg)
    temp_msg = re.sub(r' +', r' ', temp_msg)
    # Caso 5: �
    temp_msg = re.sub(r'�', r' � ', temp_msg)
    temp_msg = re.sub(r' +', r' ', temp_msg)
    # Caso monto y divisas
    temp_msg = re.sub(r'(\b\d+)(s)', r'\1 \2', temp_msg)
    # ---------------------------------------------------------------------------------------
    # Adición de espacios para separar caracteres especiales al final del texto
    temp_msg = re.sub(r'^(.+)(\W)$', r'\1 \2', temp_msg, flags=re.M)
    temp_msg = re.sub(r' +', r' ', temp_msg)
    # ---------------------------------------------------------------------------------------
    # Escribir puntos suspensivos
    temp_msg = re.sub(r'Puntos_suspensivoS', r'...', temp_msg)
    # ---------------------------------------------------------------------------------------
    # Separación en tokens
    preprocessed_msg = temp_msg.split()
    return preprocessed_msg


def get_new_ner_tags(t1, t2, ner1):
    l1 = preprocess_message(t1)
    l2 = preprocess_message(t2)
    dif = DeepDiff(l1, l2)
    indexes1 = list(range(len(l1)))
    if 'iterable_item_removed' in dif.keys():
        for k in dif['iterable_item_removed']:
            indexes1.remove(int(re.sub(r'root\[(\d+)\]', r'\1', k)))
        ner = [ner1[idx] for idx in indexes1]
    else:
        ner = ner1
    ner2 = [100] * len(l2)
    if 'iterable_item_added' in dif.keys():
        for k in dif['iterable_item_added']:
            ner2[int(re.sub(r'root\[(\d+)\]', r'\1', k))] = 0
    idx = 0
    for i, n in enumerate(ner2):
        if n == 100:
            ner2[i] = ner[idx]
            idx += 1
    return ner2


with open('train_nlu_data.json') as file:
    data = json.load(file)


new_lista = []
with open('new_train_nlu_data.json', 'w') as file:
    json.dump(new_lista, file, indent=4)

for dictionary in data:
    # Caso: "curso de " ---> "curso " en su primera coincidencia dentro del texto
    new_dictionary_1 = dictionary.copy()
    if new_dictionary_1['entities']:
        for i in range(len(new_dictionary_1['entities'])):
            entity_dict = new_dictionary_1['entities'][i]
            if (entity_dict['entity'] == 'nombre_curso') or (entity_dict['entity'] == 'nombre_programa'):
                string = new_dictionary_1['text']
                ner_tags_orig = new_dictionary_1['ner_tags']
                # print('string: ', string)
                # print('ner_tags_orig: ', ner_tags_orig)
                if entity_dict['entity'] == 'nombre_curso':
                    new_string = re.sub(r'curso de ' + entity_dict['value'],
                                        r'curso ' + entity_dict['value'], string, count=1)
                    new_dictionary_1['text'] = new_string
                    for j, entity in enumerate(new_dictionary_1['entities']):
                        if entity['span_start'] >= entity_dict['span_start']:
                            new_dictionary_1['entities'][i]['span_start'] -= 3
                            new_dictionary_1['entities'][i]['span_end'] -= 3
                    new_dictionary_1['ner_tags'] = get_new_ner_tags(string, new_string, ner_tags_orig)
                    new_dictionary_1["preprocessed_message"] = preprocess_message(new_string)
                    new_dictionary_1["tokens"] = preprocess_message(new_string)
                    # print('new_ner_tags: ', new_dictionary_1['ner_tags'])
                    # print('new_string: ', new_string)
                    with open('new_train_nlu_data.json', 'r+') as file:
                        data = json.load(file)
                        data.append(new_dictionary_1)
                        file.seek(0)
                        json.dump(data, file, indent=4)

    # Caso: "curso de " ---> "curso " cuando aparece al final del texto
    new_dictionary_2 = dictionary.copy()
    if new_dictionary_2['entities']:
        for i in range(len(new_dictionary_2['entities'])):
            entity_dict = new_dictionary_2['entities'][i]
            if (entity_dict['entity'] == 'nombre_curso') or (entity_dict['entity'] == 'nombre_programa'):
                string = new_dictionary_2['text']
                if entity_dict['entity'] == 'nombre_curso':
                    if re.search(r'curso de ' + entity_dict['value'] + r'$', string):
                        new_string = re.sub(r'curso de ' + entity_dict['value'] + r'$',
                                            r'curso: ' + entity_dict['value'], string, count=1)
                        new_dictionary_2['text'] = new_string
                        for j, entity in enumerate(new_dictionary_2['entities']):
                            if entity['span_start'] >= entity_dict['span_start']:
                                new_dictionary_2['entities'][i]['span_start'] -= 2
                                new_dictionary_2['entities'][i]['span_end'] -= 2
                        new_dictionary_2["preprocessed_message"] = preprocess_message(new_string)
                        new_dictionary_2["tokens"] = preprocess_message(new_string)
                        with open('new_train_nlu_data.json', 'r+') as file:
                            data = json.load(file)
                            data.append(new_dictionary_2)
                            file.seek(0)
                            json.dump(data, file, indent=4)

    # Caso: "costo" ---> " precio " en su primera coincidencia dentro del texto
    new_dictionary_3 = dictionary.copy()
    if new_dictionary_3['intent'] == 'informacion_precio':
        if new_dictionary_3['text']:
            string = new_dictionary_3['text']
            # print('original: ', string)
            new_dictionary_3['text'] = re.sub(r'costo', r'precio', new_dictionary_3['text'], count=1)
            new_dictionary_3['text'] = re.sub(r'Costo', r'Precio', new_dictionary_3['text'], count=1)
            new_string = new_dictionary_3['text']
            new_dictionary_3["preprocessed_message"] = preprocess_message(new_string)
            new_dictionary_3["tokens"] = preprocess_message(new_string)
            with open('new_train_nlu_data.json', 'r+') as file:
                data = json.load(file)
                data.append(new_dictionary_3)
                file.seek(0)
                json.dump(data, file, indent=4)

    # Caso: 'Cuánto cuesta', 'Cuánto está', 'cuanto esta', 'cuanto cuesta', 'Cual es el costo' --->
    # " cuanto se debe pagar por " y otras coincidencias dentro del texto
    new_dictionary_4 = dictionary.copy()
    if new_dictionary_4['intent'] == 'informacion_precio':
        exp_ = ['Cuánto cuesta', 'Cuánto está', 'cuanto esta', 'cuanto cuesta', 'Cual es el costo']
        combined_exp_ = r'|'.join(map(r'(?:{})'.format, exp_))
        if re.search(combined_exp_, new_dictionary_4['text']):
            string = new_dictionary_4['text']
            ner_tags_orig = new_dictionary_4['ner_tags']
            if string not in text_info_precio:
                text_info_precio.append(string)
                # print(text_info_precio[-1])
                new_dictionary_4['text'] = re.sub(combined_exp_, r'cuanto se debe pagar por', string, count=1)
                new_string = new_dictionary_4['text']
                new_dictionary_4['ner_tags'] = get_new_ner_tags(string, new_string, ner_tags_orig)
                new_dictionary_4["preprocessed_message"] = preprocess_message(new_string)
                new_dictionary_4["tokens"] = preprocess_message(new_string)
                with open('new_train_nlu_data.json', 'r+') as file:
                    data = json.load(file)
                    data.append(new_dictionary_4)
                    file.seek(0)
                    json.dump(data, file, indent=4)
                new_dictionary_4['text'] = re.sub(combined_exp_, r'cuanto debo cancelar por', string, count=1)
                new_string = new_dictionary_4['text']
                new_dictionary_4['ner_tags'] = get_new_ner_tags(string, new_string, ner_tags_orig)
                new_dictionary_4["preprocessed_message"] = preprocess_message(new_string)
                new_dictionary_4["tokens"] = preprocess_message(new_string)
                with open('new_train_nlu_data.json', 'r+') as file:
                    data = json.load(file)
                    data.append(new_dictionary_4)
                    file.seek(0)
                    json.dump(data, file, indent=4)
                new_dictionary_4['text'] = re.sub(combined_exp_, r'cuanto se cancela por', string, count=1)
                new_string = new_dictionary_4['text']
                new_dictionary_4['ner_tags'] = get_new_ner_tags(string, new_string, ner_tags_orig)
                new_dictionary_4["preprocessed_message"] = preprocess_message(new_string)
                new_dictionary_4["tokens"] = preprocess_message(new_string)
                with open('new_train_nlu_data.json', 'r+') as file:
                    data = json.load(file)
                    data.append(new_dictionary_4)
                    file.seek(0)
                    json.dump(data, file, indent=4)
                new_dictionary_4['text'] = re.sub(combined_exp_, r'cuanto es lo que se paga por', string, count=1)
                new_string = new_dictionary_4['text']
                new_dictionary_4['ner_tags'] = get_new_ner_tags(string, new_string, ner_tags_orig)
                new_dictionary_4["preprocessed_message"] = preprocess_message(new_string)
                new_dictionary_4["tokens"] = preprocess_message(new_string)
                with open('new_train_nlu_data.json', 'r+') as file:
                    data = json.load(file)
                    data.append(new_dictionary_4)
                    file.seek(0)
                    json.dump(data, file, indent=4)
                new_dictionary_4['text'] = re.sub(combined_exp_, r'cuanto se tiene que pagar por', string, count=1)
                new_string = new_dictionary_4['text']
                new_dictionary_4['ner_tags'] = get_new_ner_tags(string, new_string, ner_tags_orig)
                new_dictionary_4["preprocessed_message"] = preprocess_message(new_string)
                new_dictionary_4["tokens"] = preprocess_message(new_string)
                # print(new_dictionary_4['text'])
                # print('-----------------------------------------------------------------------')
                with open('new_train_nlu_data.json', 'r+') as file:
                    data = json.load(file)
                    data.append(new_dictionary_4)
                    file.seek(0)
                    json.dump(data, file, indent=4)

# Caso: informacion_precio ADICIONALES
questions_info_precio = ['cuanto sería el pago?', 'cuánto se tiene que cancelar?', 'cuánto se tiene que cancelar',
                       'cuánto se tiene que pagar?', 'cuánto se tiene que pagar']
add_dict_info_precio = dict()

for question in questions_info_precio:
    add_dict_info_precio["text"] = question
    add_dict_info_precio["intent"] = "informacion_precio"
    add_dict_info_precio["entities"] = []
    add_dict_info_precio["preprocessed_message"] = preprocess_message(question)
    add_dict_info_precio["tokens"] = preprocess_message(question)
    add_dict_info_precio["ner_tags"] = [0 for idx in add_dict_info_precio["preprocessed_message"]]
    add_dict_info_precio["intent_label"] = 2
    with open('new_train_nlu_data.json', 'r+') as file:
        data = json.load(file)
        data.append(add_dict_info_precio)
        file.seek(0)
        json.dump(data, file, indent=4)

# Caso: informacion_pago
questions_info_pago = ['dónde hago el depósito?', 'donde hago el depósito', 'cuando hago el depósito?',
                       'cuando hago el depósito', 'donde hago la transferencia', 'como hago la transferencia',
                       'como realizo la transferencia', 'quiero hacer la transferencia?']
add_dict_info_pago = dict()

for question in questions_info_pago:
    add_dict_info_pago["text"] = question
    add_dict_info_pago["intent"] = "informacion_pago"
    add_dict_info_pago["entities"] = []
    add_dict_info_pago["preprocessed_message"] = preprocess_message(question)
    add_dict_info_pago["tokens"] = preprocess_message(question)
    add_dict_info_pago["ner_tags"] = [0 for idx in add_dict_info_pago["preprocessed_message"]]
    add_dict_info_pago["intent_label"] = 7
    with open('new_train_nlu_data.json', 'r+') as file:
        data = json.load(file)
        data.append(add_dict_info_pago)
        file.seek(0)
        json.dump(data, file, indent=4)

# Caso: informacion_inscripcion
questions_info_inscripcion = ['cómo me inscribo', 'aun hay vacantes']
add_dict_info_inscripcion = dict()

for question in questions_info_inscripcion:
    add_dict_info_inscripcion["text"] = question
    add_dict_info_inscripcion["intent"] = "informacion_inscripcion"
    add_dict_info_inscripcion["entities"] = []
    add_dict_info_inscripcion["preprocessed_message"] = preprocess_message(question)
    add_dict_info_inscripcion["tokens"] = preprocess_message(question)
    add_dict_info_inscripcion["ner_tags"] = [0 for idx in add_dict_info_inscripcion["preprocessed_message"]]
    add_dict_info_inscripcion["intent_label"] = 5
    with open('new_train_nlu_data.json', 'r+') as file:
        data = json.load(file)
        data.append(add_dict_info_inscripcion)
        file.seek(0)
        json.dump(data, file, indent=4)

# Caso: informacion_programacion
questions_info_programacion = ['cual es la programación del curso?', 'qué días se dicta?', 'en qué días?',
                               'cómo es la programación del curso?', 'en qué días', 'qué días?', 'qué días',
                               'cuáles días?', 'cuáles días se enseña?', 'cuáles días se enseña',
                               'me podría decir los días de dictado?', 'me puede decir qué días se dicta?',
                               'me puede decir qué días se enseña?', 'me puede decir qué días enseñan',
                               'qué día está programado?']
add_dict_info_programacion = dict()

for question in questions_info_programacion:
    add_dict_info_programacion["text"] = question
    add_dict_info_programacion["intent"] = "informacion_programacion"
    add_dict_info_programacion["entities"] = []
    add_dict_info_programacion["preprocessed_message"] = preprocess_message(question)
    add_dict_info_programacion["tokens"] = preprocess_message(question)
    add_dict_info_programacion["ner_tags"] = [0 for idx in add_dict_info_programacion["preprocessed_message"]]
    add_dict_info_programacion["intent_label"] = 6
    # print(add_dict_info_programacion)
    with open('new_train_nlu_data.json', 'r+') as file:
        data = json.load(file)
        data.append(add_dict_info_programacion)
        file.seek(0)
        json.dump(data, file, indent=4)







