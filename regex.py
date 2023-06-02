
import re
from deepdiff import DeepDiff


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



# text1 = 'I have called the service desk 100 times and nobody replies to me. I need a conversation ASAP!! My number ' \
#        'is 111-1234567! My other number is 7654321!'
# result1 = re.findall(r'\d{3}-\d{7}|\d{7}', text1)
# # print('result1: ', result1)
#
# text2 = '111-1234567! That is my number! The other one is 7654321!'
# result2 = re.findall(r'^\d{3}-\d{7}|^\d{7}', text2)
# # print('result2: ', result2)
#
# text3 = 'abcabc aa cc dd e 123123 abcabab'
# result3 = re.findall(r'(\w{3})(\1)', text3)
# # print('result3: ', result3)
# result4 = re.findall(r'(\w{3})(\w{2})(\2)', text3)
# # print('result4: ', result4)
#
# temp_msg = 'Hola, me gustaria informacion acerca del curso de Redes de Fibra Optica, mi correo es elfula.nito@gmail.com ' \
#          'y soy de la facultad de ingenieria electrica de la UNI.Gracias'
# # reg = re.findall(, prueba)
#
#
# email_match = re.search(r'\w+(?:\.\w+)*@\w+(?:\.\w+)+', temp_msg)
# if email_match:
#     l, u = email_match.span()
#     # print(l,u)
#     pre = temp_msg[:l]
#     # print(pre)
#     post = temp_msg[u:]
#     # print(post)
#     new_email = re.sub(r'\.', r'*.*', temp_msg[l:u])
#     temp_msg = pre + new_email + post
#     # print(temp_msg)
#
# temp_msg = re.sub(r'([a-zA-Z])(\.)([a-zA-Z])', r'\1 \2 \3', temp_msg)
# print(temp_msg)
#
# if email_match:
#     temp_msg = re.sub(r'\\\.\\', r'.', temp_msg)
#     print(temp_msg)

test1 = {
        "text": "favor informacion sobre el curso de CCTV que inicia el 21 de Febrero",
        "intent": "informacion_general",
        "entities": [
            {
                "value": "curso",
                "entity": "tipo_capacitacion",
                "span_start": 27,
                "span_end": 32
            },
            {
                "value": "CCTV",
                "entity": "nombre_curso",
                "span_start": 36,
                "span_end": 40
            }
        ],
        "preprocessed_message": [
            "favor",
            "informacion",
            "sobre",
            "el",
            "curso",
            "de",
            "CCTV",
            "que",
            "inicia",
            "el",
            "21",
            "de",
            "Febrero"
        ],
        "tokens": [
            "favor",
            "informacion",
            "sobre",
            "el",
            "curso",
            "de",
            "CCTV",
            "que",
            "inicia",
            "el",
            "21",
            "de",
            "Febrero"
        ],
        "ner_tags": [
            0,
            0,
            0,
            0,
            3,
            0,
            1,
            0,
            0,
            0,
            0,
            0,
            0
        ],
        "intent_label": 0
    }

test2 = {
        "text": "Y hay el programa de especialista en sjsutrma de seguridad electr\u00f3nica?",
        "intent": "informacion_general",
        "entities": [
            {
                "value": "programa",
                "entity": "tipo_capacitacion",
                "span_start": 9,
                "span_end": 17
            },
            {
                "value": "especialista en sjsutrma de seguridad electr\u00f3nica",
                "entity": "nombre_curso",
                "span_start": 21,
                "span_end": 70
            }
        ],
        "preprocessed_message": [
            "Y",
            "hay",
            "el",
            "programa",
            "de",
            "especialista",
            "en",
            "sjsutrma",
            "de",
            "seguridad",
            "electr\u00f3nica",
            "?"
        ],
        "tokens": [
            "Y",
            "hay",
            "el",
            "programa",
            "de",
            "especialista",
            "en",
            "sjsutrma",
            "de",
            "seguridad",
            "electr\u00f3nica",
            "?"
        ],
        "ner_tags": [
            0,
            0,
            0,
            3,
            0,
            1,
            2,
            2,
            2,
            2,
            2,
            0
        ],
        "intent_label": 0
    }


# def replace(match):
#     if match:
#         if match.group() == 'curso de ' + elem['value']:
#             return 'curso ' + elem['value']
#         # else:
#         #     return 'programa ' + elem['value']


# string = "favor informacion sobre el curso de CCTV que inicia el 21 de Febrero"
# #string = "quisiera por favor información del curso de cableado estructurado de cobre"
# new_dict = dict()
# i = 0
# for elem in test1["entities"]:
#     if elem['entity'] == 'nombre_curso':
#         print(test1['text'])
#         new_string1 = re.sub('curso de ' + elem['value'], 'curso ' + elem['value'], string)
#         print(new_string1)
#         # new_string2 = re.sub('programa de ' + elem['value'], replace, string)
#         # print(new_string2)
#         # test_i = test1.copy()
#         # test_i['text'] = new_string1
#         # i = i+1
#         # print("test_" + str(i) + ": ", test_i)


# Problema de comparación de listas


# def ners_tag_new(msg_A, msg_B, ner_tags_A):
#     """
#     Genera la lista ner_tags para el nuevo texto generado.
#     :param tokens_list: lista de tokens del texto original
#     :param near_tags: lista de tags del texto generado
#     :return: near_tags_new
#     """
#     tokens_list_A = preprocess_message(msg_A)
#     tokens_list_B = preprocess_message(msg_B)
#     ddiff = DeepDiff(tokens_list_A, tokens_list_B)
#     print('tokens_list_A: ', tokens_list_A)
#     print('tokens_list_B: ', tokens_list_B)
#     print('ddiff: ', ddiff)
#     print('ner_tags_A: ', ner_tags_A)
#     dictionary_tokens_ners_A = {}
#     dictionary_tokens_ners_B_order = dict()
#     for key in tokens_list_A:
#         for value in ner_tags_A:
#             dictionary_tokens_ners_A[key] = value
#             ner_tags_A.remove(value)
#             break
#     print('dictionary_tokens_ners_A: ', dictionary_tokens_ners_A)
#     if ddiff['iterable_item_removed']:
#         for key_ddiff_removed, value_ddiff_removed in ddiff['iterable_item_removed'].items():
#             del dictionary_tokens_ners_A[value_ddiff_removed]
#     if ddiff['iterable_item_added']:
#         for key_ddiff_added, value_ddiff_added in ddiff['iterable_item_added'].items():
#             dictionary_tokens_ners_A[value_ddiff_added] = 0
#     if ddiff['values_changed']:
#         for key_ddiff_changed, value_ddiff_changed in ddiff['values_changed'].items():
#             # print(key_ddiff_changed, value_ddiff_changed)
#             for k, v in value_ddiff_changed.items():
#                 if k == 'new_value':
#                     dictionary_tokens_ners_A[v] = 0
#     for key_list_B in tokens_list_B:
#         val = dictionary_tokens_ners_A[key_list_B]
#         dictionary_tokens_ners_B_order[key_list_B] = val
#     ner_tags_B = dictionary_tokens_ners_B_order.values()
#     print('dictionary_tokens_ners_B_order: ', dictionary_tokens_ners_B_order)
#     print('ner_tags_B: ', list(ner_tags_B))
#
#
# # a = 'Me podría brindar información acerca del curso de Machine Learning?'
# # b = 'Me podría brindar información acerca del curso Machine Learning para principiantes?'
# # ner_tags_A = [0, 0, 0, 0, 0, 0, 3, 0, 1, 2, 0]
# # ners_tag_new(a, b, ner_tags_A)
#
# a = 'Quisiera información acerca de este curso: Machine Learning'
# b = 'Me podría brindar información acerca del curso Machine Learning?'
# ner_tags_A = [0, 0, 0, 0, 0, 3, 0, 1, 2]
# ners_tag_new(a, b, ner_tags_A)
#
# # # Ordenando un dicionario por keys conforme a una lista establecida
# # tokens_list_B = ['Me', 'podría', 'brindar', 'información', 'acerca', 'del', 'curso', 'Machine', 'Learning', '?']
# # dictionary_tokens_ners_B = {'Quisiera': 0, 'información': 0, 'acerca': 0, 'de': 0, 'curso': 3, 'Machine': 1, 'Learning': 2, 'podría': 0, 'brindar': 0, '?': 0, 'Me': 0, 'del': 0}
# #
# # dictionary_tokens_ners_B_order = dict()
# # for key_list_B in tokens_list_B:
# #     val = dictionary_tokens_ners_B[key_list_B]
# #     dictionary_tokens_ners_B_order[key_list_B] = val
# # print(dictionary_tokens_ners_B_order)


t1 = 'Quisiera de información acerca de este curso de Machine Learning'
t2 = 'Me podría brindar información acerca del curso Machine Learning?'
ner_tags_A = [0, 0, 0, 0, 0, 0, 3, 0, 1, 2]


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


ner2 = get_new_ner_tags(t1, t2, ner_tags_A)
print(ner2)