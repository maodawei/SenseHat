import json
import pandas as pd


with open('config.json', 'r') as file_name:
    json_data = json.load(file_name)
    
    min_temperature = json_data['min_temperature']
    max_temperature = json_data['max_temperature']
    min_humidity = json_data['min_humidity']
    max_humidity = json_data['max_humidity']
    
    row_l = ['2019-03-27 10:29:14', 21, 55]

    column_names = ['date', 'status']
    date = row_l[0].split()[0]
 
    # check if the temperature and the humidity are within the specified range in the json file
    if ((row_l[1] > min_temperature) and (row_l[1] < max_temperature)) and ((row_l[2] > min_humidity) and (row_l[2] < max_humidity)):
        # if both temperature and humidity are within the specified range, then set status to 'OK'
        status = 'OK'
    # if temperature is less than the specified minimum temperature, then write a message to the status
    elif(row_l[1] < min_temperature):
        # define a variables and calculate the difference between the minumim temperature and the stored temperature
        temp_difference = min_temperature - row_l[1]
        # write a message to status 
        status = 'BAD: ' + temp_difference + ' *C below minimum temperature'
    # if temperature is more than the specified maximum temperature, then write a message to the status
    elif(row_l[1] > max_temperature):
        # define a variables and calculate the difference between the maximum temperature and the stored temperature
        temp_difference = row_l[1] - min_temperature
        # write a message to status 
        status = 'BAD: ' + temp_difference + ' *C above maximum temperature'
    # if humidity is less than the specified minimum humidity, then write a message to the status
    elif(row_l[2] < min_humidity):
        # define a variables and calculate the difference between the maximum humidity and the stored humidity
        temp_difference = min_humidity - row_l[2]
        # write a message to status
        status = 'BAD: ' + temp_difference + ' *C below minimum humidity'
    # if humidity is more than the specified maximum humidity, then write a message to the status
    elif(row_l[1] > max_humidity):
        # define a variables and calculate the difference between the maximum humidity and the stored humidity
        temp_difference = row_l[2] - max_humidity
        # write a message to status
        status = 'BAD: ' + temp_difference + ' *C above maximum humidity'
    
    # create a pandas dataframe and store the date and the status to it
    df = pd.DataFrame([date, status], column_names).T
    print(df.head())

    # save the dataframe to a csv file
    df.to_csv('report.csv')