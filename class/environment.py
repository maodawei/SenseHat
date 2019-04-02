# import packages
import sqlite3
from datetime import datetime
# from crontab import CronTab
from sense_hat import SenseHat
import os
import time
import requests
import json
import os
import json
from db import database
from readjson import jsonreading
import notification from notification
class temperature():
    @staticmethod
    def get_cpu_temp():
        res = os.popen("vcgencmd measure_temp").readline()
        t = float(res.replace("temp=","").replace("'C\n",""))
        return(t)
    
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
    
    @staticmethod
    def check_temp_hum(file_name):
        min_temperature, max_temperature, min_humidity, max_humidity =jsonreading.read_json(file_name)
        sensehat_row=database.getEnvironmentData()
        if(sensehat_row[1] > min_temperature and sensehat_row[1] < max_temperature and sensehat_row[2] > min_humidity and sensehat_row[2] < max_humidity):
            print (sensehat_row)
        else:
            notification.execute_notification()
            database.insertNotificationTime()
    