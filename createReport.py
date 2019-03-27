# import packages
import sqlite3
import pandas as pd
import json


# initialize databse name
dbname = 'sensehat.db'

# read the data from the databse
def read_data(dbname):

    conn=sqlite3.connect(dbname)
    curs=conn.cursor()
    for row in curs.execute("SELECT * FROM SENSEHAT_data"):
        row_l = list(row)
        date = row_l[0].split()[0]
        temp = row_l[1]
        hum = row_l[2]
    return date, temp, hum


def read_json(file_name):
    with open(file_name, 'r') as json_file:
        json_data = json.load(json_file)

        min_temperature = json_data['min_temperature']
        max_temperature = json_data['max_temperature']
        min_humidity = json_data['min_humidity']
        max_humidity = json_data['max_humidity']
        
    return min_temperature, max_temperature, min_humidity, max_humidity


def check_status(file_name):

    # read a function and split the return values into four variables
    min_temperature, max_temperature, min_humidity, max_humidity = read_json(file_name)

    date, temp, hum = read_data(dbname)

    # check if the temperature and the humidity are within the specified range in the json file
    if ((temp > min_temperature) and (temp < max_temperature)) and ((hum > min_humidity) and (hum < max_humidity)):
        # if both temperature and humidity are within the specified range, then set status to 'OK'
        status = 'OK'
    # if temperature is less than the specified minimum temperature, then write a message to the status
    elif(temp < min_temperature):
        # define a variables and calculate the difference between the minumim temperature and the stored temperature
        temp_difference = min_temperature - temp
        # write a message to status 
        status = 'BAD: ' + temp_difference + ' *C below minimum temperature'
    # if temperature is more than the specified maximum temperature, then write a message to the status
    elif(temp > max_temperature):
        # define a variables and calculate the difference between the maximum temperature and the stored temperature
        temp_difference = temp - min_temperature
        # write a message to status 
        status = 'BAD: ' + temp_difference + ' *C above maximum temperature'
    # if humidity is less than the specified minimum humidity, then write a message to the status
    elif(hum < min_humidity):
        # define a variables and calculate the difference between the maximum humidity and the stored humidity
        hum_difference = min_humidity - hum
        # write a message to status
        status = 'BAD: ' + hum_difference + ' below minimum humidity'
    # if humidity is more than the specified maximum humidity, then write a message to the status
    elif(hum > max_humidity):
        # define a variables and calculate the difference between the maximum humidity and the stored humidity
        hum_difference = hum - max_humidity
        # write a message to status
        status = 'BAD: ' + hum_difference + ' above maximum humidity'
    
    return date, status


def write_to_df(file_name='config.json'):

    date, status = check_status(file_name)
    # create a dataframe
    df = pd.DataFrame((date, status), ['Date', 'Status'])
    # write the dataframe to a csv file
    df.to_csv('report.csv')


write_to_df()