import json
import os
import requests

class jsonreading:
    
    @staticmethod
    def read_json(file_name):
        """
        This function accepts one parameter: json file name
        retrieve everthing in the file and return its contents 
        For the purpose of this assignment, the json file includes
        minimum temperature, maximum temperature, minimum humidity, maximum humidity
        """

        with open(file_name,'r') as json_file:
            json_data=json.load(json_file)

            min_temperature=json_data['min_temperature']
            max_temperature=json_data['max_temperature']
            min_humidity=json_data['min_humidity']
            max_humidity=json_data['max_humidity']
        return min_temperature, max_temperature, min_humidity, max_humidity
        