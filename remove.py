import json
import re


with open('train_nlu_data.json') as file:
    data = json.load(file)

count_info_general = 0
count_info_precio = 0
counter_dic = 0
documents = []

for i, dictionary in enumerate(data):
    if dictionary['intent'] == 'informacion_general':
        if re.search(r'Quiero más información sobre esta escuela', dictionary['text']):
            if count_info_general == 0:
                documents.append(dictionary)
                count_info_general += 1
        else:
            documents.append(dictionary)
    elif dictionary['intent'] == 'informacion_precio':
        if re.search(r'¿Cuánto cuesta esta escuela', dictionary['text']):
            if count_info_precio == 0:
                documents.append(dictionary)
                count_info_precio += 1
    else:
        documents.append(dictionary)
    print('procesando ' + str(i) + ' diccionarios...')

with open('remove_train_nlu_data.json', 'w') as file:
    json.dump(documents, file, indent=4)

