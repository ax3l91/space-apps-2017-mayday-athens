import json

with open('Data/test.json') as json_data:
    data = json.load(json_data)
    for element in data: 
        del element['type']