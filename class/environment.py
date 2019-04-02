# import packages
# from crontab import CronTab
from sense_hat import SenseHat
import os
from db import database
from readjson import jsonreading
from notification import notification

class temperature:

    @staticmethod
    def get_cpu_temp():
        res = os.popen("vcgencmd measure_temp").readline()
        t = float(res.replace("temp=","").replace("'C\n",""))
        return(t)
    
    # this function correct the temperature and return both temperature and humidity
    @staticmethod
    def measure_temp_hum():
        # initialize the sense hat object
        sense = SenseHat()
        # get the temperature
        t = sense.get_temperature_from_humidity()
        # get the cpu temerature
        t_cpu = temperature.get_cpu_temp()
        # get humidity
        h = sense.get_humidity()
        # calculates the real temperature compesating CPU heating
        t_corr = t - ((t_cpu-t)/1.5)
        # print("t=%.1f  t_cpu=%.1f  t_corr=%.1f  h=%d  p=%d" % (t, t_cpu, t_corr, round(h)))
        # return both termpreature after correction and humidity
        return round(t_corr), round(h)
    
    # this function checks the humidity and temperature if either is out the specified range in the json file
    @staticmethod
    def check_temp_hum(file_name):
        # call the read_json from jsonreading class which returns:
        # 1) minimum temperature
        # 2) maximum temperature
        # 3) minimum humidity
        # 4) maximum humidity
        min_temperature, max_temperature, min_humidity, max_humidity =jsonreading.read_json(file_name)
        # call the function getEnvironmentData from the database class
        # which would return current temperature and humidity
        sensehat_temp, sensehat_hum = database.getEnvironmentData()
        # check if the current temperature and humidity is within the specified range
        if(sensehat_temp > min_temperature and sensehat_temp < max_temperature and sensehat_hum > min_humidity and sensehat_hum < max_humidity):
            # if current temperature and humidity is within the range, print them
            print('Current temperature: ', sensehat_temp, ', current humidity: ', sensehat_hum)
        # if either is out of the range, then call the execute_notification from the notification class
        else:
            notification.execute_notification()
    