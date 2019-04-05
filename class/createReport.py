# import packages
import sqlite3
import json
import csv
from readjson import jsonreading
from db import database


# class database
class report:
    # initialize three lists to hold only all data for each date
    curr_date_list = []
    curr_temp_list = []
    curr_hum_list = []
    date = []
    temp = []
    status = []
    # this function will return a list of temperature and status
    @staticmethod
    def return_rows(file_name):
        # call the getEnvironmentData from database class and assigne the desired values to a variable
        sensehat_data_results, _, _ = database.getEnvironmentData()
        
        # initialize three lists to hold only one data for each date
        date = []
        temp = []
        status = []

        # initialize three lists to hold only all data for each date
        curr_date_list = []
        curr_temp_list = []
        curr_hum_list = []
        
        # loop through the list of sql table results
        for i in range(len(sensehat_data_results) -1):
            # check if one row is the same as the one following it
            if sensehat_data_results[i+1] != sensehat_data_results[-1]:
                if sensehat_data_results[i][0].split()[0] == sensehat_data_results[i+1][0].split()[0]:
                        # extract the date to a variable names row_date
                        row_date = sensehat_data_results[i][0].split()[0]
                        # extract the temperature to a variable names row_temp
                        row_temp = sensehat_data_results[i][1]
                        # extract the humidity to a variable names row_hum
                        row_hum = sensehat_data_results[i][2]
                        # append the date of each row to the date list that we initalized at the top
                        curr_date_list.append(row_date)
                        # append the temperature of each row to the curr_temp_list list that we initalized at the top
                        curr_temp_list.append(row_temp)
                        # append the humidity of each row to the curr_hum_list list that we initalized at the top
                        curr_hum_list.append(row_hum)

                elif sensehat_data_results[i][0].split()[0] != sensehat_data_results[i+1][0].split()[0]:
                    report.appendList(i,curr_date_list,curr_temp_list,curr_hum_list,sensehat_data_results)
                    # assign maximum and minimum temperature and humidity 
                    min_row_temp = min(curr_temp_list)
                    max_row_temp = max(curr_temp_list)
                    min_row_hum = min(curr_hum_list)
                    max_row_hum = max(curr_hum_list)
                    # call the function check_status with the max $ min temperature and humidity
                    #will get in return a status that describes that day
                    row_status = report.check_status(file_name, min_row_temp, max_row_temp,  min_row_hum, max_row_hum)
                    # append the date of each row to the date list that we initalized at the top
                    date.append(row_date)
                    # append the temperature of each row to the temp list that we initalized at the top
                    temp.append(row_temp)
                    # append the status of each row to the status list that we initalized at the top
                    status.append(row_status)
                    report.clearList(curr_date_list,curr_temp_list,curr_hum_list)
                # what if the data is only for one day!! it won't go inside the else statement
                # we need to figure this part out
                
            else:
                print('LAST ONE')
                report.appendList(i,curr_date_list,curr_temp_list,curr_hum_list,sensehat_data_results)
                # assign maximum and minimum temperature and humidity 
                min_row_temp = min(curr_temp_list)
                max_row_temp = max(curr_temp_list)
                min_row_hum = min(curr_hum_list)
                max_row_hum = max(curr_hum_list)
                # call the function check_status with the max $ min temperature and humidity
                # will get in return a status that describes that day
                row_status = report.check_status(file_name, min_row_temp, max_row_temp,  min_row_hum, max_row_hum)
                # append the date of each row to the date list that we initalized at the top
                date.append(row_date)
                # append the temperature of each row to the temp list that we initalized at the top
                temp.append(row_temp)
                # append the status of each row to the status list that we initalized at the top
                status.append(row_status)
                report.clearList(curr_date_list,curr_temp_list,curr_hum_list)

        # return date and status
        return date, status  
    
    
    @staticmethod
    def check_status(file_name, min_temp, max_temp, min_hum, max_hum):
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
        min_temperature, max_temperature, min_humidity, max_humidity =jsonreading.read_json(file_name)
        
        # instantiate variables ok & bad for the first word of the status
        ok = 'OK'
        bad = 'BAD:'

        # check if the temperature and the humidity are within the specified range in the json file
        if ((min_temp > min_temperature) and (max_temp < max_temperature)) and ((min_hum > min_humidity) and (max_hum < max_humidity)):
            # if both temperature and humidity are within the specified range, then set status to 'OK'
            status = ok
        # if either temperature or humidity is out of the range enter the else statement
        else:
            status = bad
            # check if minimum temperature is below the minimum temperature in the specified range
            if min_temp < min_temperature:
                # calculate the difference between the minumim temperature in the range and the stored temperature
                temp_difference = min_temperature - min_temp
                # add a message to the status
                status = status + str(temp_difference) + ' *C below minimum temperature and'
            # check if maximum temperature is above the maximum temperature in the specified range
            if max_temp > max_temperature:
                # calculate the difference between the maximum temperature in the range and the stored temperature
                temp_difference = max_temp - min_temperature
                # add a message to status 
                status = status + str(temp_difference) + ' *C above maximum temperature and'
            # check if minimum humidity is above the minimum humidity in the specified range
            if min_hum < min_humidity:
                # calculate the difference between the minimum humidity in the range and the stored humidity
                hum_difference = min_humidity - min_hum
                # add a message to status
                status = status + str(hum_difference) + ' below minimum humidity and'
            # check if maximum humidity is above the maximum humidity in the specified range
            if max_hum > max_humidity:
                # calculate the difference between the maximum humidity in the range and the stored humidity
                hum_difference = max_hum - max_humidity
                # add a message to status
                status = status + str(hum_difference) + ' above maximum humidity and'
            # remove the last four characters, which are ' and' in the status string
            status = status[:-4]
        # return the status
        return status
    
    @staticmethod
    def log_to_csv(file_name):
        date, status = report.return_rows(file_name)
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
    
    @staticmethod
    def clearList(curr_date_list,curr_temp_list,curr_hum_list):
        # clear all lists
        curr_date_list.clear()
        curr_temp_list.clear()
        curr_hum_list.clear()