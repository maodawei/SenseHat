import json
import os
import requests

class jsonreading:
    @staticmethod
    def read_json(file_name):
        with open(file_name,'r') as json_file:
            json_data=json.load(json_file)

            min_temperature=json_data['min_temperature']
            max_temperature=json_data['max_temperature']
            min_humidity=json_data['min_humidity']
            max_humidity=json_data['max_humidity']
            return min_temperature, max_temperature, min_humidity, max_humidity
        