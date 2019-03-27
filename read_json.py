import json

with open('config.json', 'r') as file_name:
    a = json.load(file_name)
    print(a['min_temperature'])
