
import numpy as np
import json


c = 0
count = 0
count_new_dict = 0
test_dict = dict()
test_dict['informacion_general'] = 0
test_dict['informacion_precio'] = 0
test_dict['inicio_conversacion'] = 0
test_dict['agradecimiento'] = 0
test_dict['informacion_pago'] = 0
test_dict['informacion_inscripcion'] = 0
test_dict['informacion_programacion'] = 0
test_dict['otra'] = 0



list_string = ['s0', 's1', 's2', 's3', 's4', 's5']
list_questions = ['p0', 'p1', 'p2']
new_list_string = []

list_string_split = np.array_split(list_string, 3)
for array in list_string_split:
    element_string_split = list(array)
    for i, string in enumerate(element_string_split):
        print(i, string)
        for t in range(len(element_string_split)):
            new_list_string.append(list_questions[i])
print(new_list_string)

with open('train_nlu_data.json') as file:
    data = json.load(file)


for dictionary in data:
    new_dictionary = dictionary.copy()
    if new_dictionary['entities']:
        if new_dictionary['intent'] == 'informacion_general':
            test_dict['informacion_general'] = test_dict['informacion_general'] + 1
            # print(dictionary['text'])
            # print('---------------------------------------------------')
        elif new_dictionary['intent'] == 'informacion_precio':
            test_dict['informacion_precio'] = test_dict['informacion_precio'] + 1
            # print(dictionary['text'])
            # print('---------------------------------------------------')
        elif dictionary['intent'] == 'inicio_conversacion':
            test_dict['inicio_conversacion'] = test_dict['inicio_conversacion'] + 1
            # print(dictionary['text'])
            # print('---------------------------------------------------')
        elif dictionary['intent'] == 'agradecimiento':
            test_dict['agradecimiento'] = test_dict['agradecimiento'] + 1
            # print(dictionary['text'])
            # print('---------------------------------------------------')
        elif dictionary['intent'] == 'informacion_pago':
            test_dict['informacion_pago'] = test_dict['informacion_pago'] + 1
            # print(dictionary['text'])
            # print('---------------------------------------------------')
        elif dictionary['intent'] == 'informacion_inscripcion':
            test_dict['informacion_inscripcion'] = test_dict['informacion_inscripcion'] + 1
            # print(dictionary['text'])
            # print('---------------------------------------------------')
        elif dictionary['intent'] == 'informacion_programacion':
            test_dict['informacion_programacion'] = test_dict['informacion_programacion'] + 1
            # print(dictionary['text'])
            # print('---------------------------------------------------')
        elif dictionary['intent'] == 'otra':
            test_dict['otra'] = test_dict['otra'] + 1
            # print(dictionary['text'])
            # print('---------------------------------------------------')
    count = count + 1


print('Número de documentos con nombre_curso o nombre_programa: ', count)
print('Número por cada intención: ', test_dict)


