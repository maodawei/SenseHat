# import packages
import sqlite3
import json
import csv

# initialize databse name
dbname = 'sensehat.db'

# read the data from the databse to a csv file
def read_data_to_csv(dbname, file_name='config.json'):
    """
    This function is meant to read a date row by row from a database
    to a csv file.
    This function accepts two parameters:
    dbname: database name
    file_name: the jason file name that we are using to compare each row
    of the database to its content.
    """
    # establish a connection to the database
    conn=sqlite3.connect(dbname)
    # set the cursor to the top
    curs=conn.cursor()

    # initialize three lists
    date = []
    temp = []
    status = []

    # iterate over one table in the database
    for row in curs.execute("SELECT * FROM SENSEHAT_data"):
        # convert the table's row to a python list
        row_l = list(row)
        # extract the date to a variable names row_date
        row_date = row_l[0].split()[0]
        # extract the temperature to a variable names row_temp
        row_temp = row_l[1]
        # extract the humidity to a variable names row_hum
        row_hum = row_l[2]

        # append the date of each row to the date list that we initalized at the top
        date.append(row_date)
        # append the temperature of each row to the date list that we initalized at the top
        temp.append(row_temp)

        # calling another function to check the status of each day
        # by giving it a temperature and a humidity. This function returns a status
        status_now = check_status(file_name, row_temp, row_hum)
        # append the status of each row to the date list that we initalized at the top
        status.append(status_now)

    # close the connection to the database
    conn.close()

    # open a csv file if it exists, otherwise create a new one
    with open('report.csv', mode='w') as csv_file:
        # specified the delimiter between columns and quotechar for each column
        csv_file = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        # write the header of the csv file
        csv_file.writerow(["Date", "Status"])
        # iterate though the lists 'date' and 'status'
        for d, s in zip(date, status):
            # write each row of the list to the csv file
            csv_file.writerow([d, s])

# This function will read a json file and return its contents 
def read_json(file_name):
    """
    This function will read contents from json files
    parameters: file_name -> the file of the json file
    This function will return four values:
    min_temperature
    max_temperature
    min_humidity
    max_humidity
    """
    # open the exisitng json file to read only

    with open(file_name, 'r') as json_file:
        # load the file data to a variable named json_data
        json_data = json.load(json_file)
        # since the json data comes as python dictionary
        # we'll get the values of the dictionary by specifing the key
        # assign values of each key to a variable
        min_temperature = json_data['min_temperature']
        max_temperature = json_data['max_temperature']
        min_humidity = json_data['min_humidity']
        max_humidity = json_data['max_humidity']
        
    # return min_temperature, max_temperature, min_humidity, max_humidity
    return min_temperature, max_temperature, min_humidity, max_humidity


def check_status(file_name, temp, hum):
    """
    This function will check the status of one day
    based on the temperature and the humidity
    This function accepts four parameters:
    file_name: json filename since we're calling read_json function here
    temp: the temperature of one day
    hum: the humidity of one day
    This function will return the status of one day
    """
    # read a function and split the return values into four variables
    min_temperature, max_temperature, min_humidity, max_humidity = read_json(file_name)

    # check if the temperature and the humidity are within the specified range in the json file
    if ((temp > min_temperature) and (temp < max_temperature)) and ((hum > min_humidity) and (hum < max_humidity)):
        # if both temperature and humidity are within the specified range, then set status to 'OK'
        status = 'OK'
    # if temperature is less than the specified minimum temperature, then write a message to the status
    elif(temp < min_temperature):
        # define a variables and calculate the difference between the minumim temperature and the stored temperature
        temp_difference = min_temperature - temp
        # write a message to status 
        status = 'BAD: ' + str(temp_difference) + ' *C below minimum temperature'
    # if temperature is more than the specified maximum temperature, then write a message to the status
    elif(temp > max_temperature):
        # define a variables and calculate the difference between the maximum temperature and the stored temperature
        temp_difference = temp - min_temperature
        # write a message to status 
        status = 'BAD: ' + str(temp_difference) + ' *C above maximum temperature'
    # if humidity is less than the specified minimum humidity, then write a message to the status
    elif(hum < min_humidity):
        # define a variables and calculate the difference between the maximum humidity and the stored humidity
        hum_difference = min_humidity - hum
        # write a message to status
        status = 'BAD: ' + str(hum_difference) + ' below minimum humidity'
    # if humidity is more than the specified maximum humidity, then write a message to the status
    elif(hum > max_humidity):
        # define a variables and calculate the difference between the maximum humidity and the stored humidity
        hum_difference = hum - max_humidity
        # write a message to status
        status = 'BAD: ' + str(hum_difference) + ' above maximum humidity'
    
    # return the status
    return status


# call the function
read_data_to_csv(dbname, file_name='config.json')