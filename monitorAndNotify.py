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

# initialize databse name
dbname = 'sensehat.db'
# get the current time
# time = datetime.now().strftime("%H:%M")

def create_table(dbname):
  # make a connection and create a database if doesn't exist
  conn = sqlite3.connect(dbname)
  with conn: 
      # set up the cursor
      cur = conn.cursor() 
      # drop table if any exists
      cur.execute("DROP TABLE IF EXISTS SENSEHAT_data")
      # create a table to store current time, temperature, humidity
      cur.execute("CREATE TABLE SENSEHAT_data(timestamp DATETIME, temp NUMERIC, hum NUMERIC)")
  # commit changes
  conn.commit()
  # close the connection
  conn.close()

def get_cpu_temp():
  res = os.popen("vcgencmd measure_temp").readline()
  t = float(res.replace("temp=","").replace("'C\n",""))
  return(t)

def measure_temp_hum():
  # initialize the sense hat object
  sense = SenseHat()
  # get the temperature
  t = sense.get_temperature_from_humidity()
  # get the cpu temerature
  t_cpu = get_cpu_temp()
  # get humidity
  h = sense.get_humidity()

  # calculates the real temperature compesating CPU heating
  t_corr = t - ((t_cpu-t)/1.5)

  # print("t=%.1f  t_cpu=%.1f  t_corr=%.1f  h=%d  p=%d" % (t, t_cpu, t_corr, round(h)))
  # return both termpreature after correction and humidity
  return round(t_corr), round(h)

# log sensor data on database
def logData(dbname, measure_temp_hum):
  # extract both termpreature and humidity from the function measure_temp_hum
  temp, hum = measure_temp_hum()

  # make a connection and create a database if doesn't exist
  conn = sqlite3.connect(dbname)
  # set up the cursor
  curs = conn.cursor()
  # insert data into the table
  curs.execute("INSERT INTO SENSEHAT_data values(datetime('now'), ?, ?)", (temp,hum))
  # commit changes
  conn.commit()
  # close the connection
  conn.close()

# display database data
def displayData(dbname):
  conn=sqlite3.connect(dbname)
  curs=conn.cursor()
  print ("\nEntire database contents:\n")
  for row in curs.execute("SELECT * FROM SENSEHAT_data"):
      print (row)
  conn.close()


# check the temperature or humidity
def check_temp_hum(dbname, file_name):

  def read_json(file_name):
    with open(file_name, 'r') as json_file:
      json_data = json.load(json_file)

      min_temperature = json_data['min_temperature']
      max_temperature = json_data['max_temperature']
      min_humidity = json_data['min_humidity']
      max_humidity = json_data['max_humidity']

      return min_temperature, max_temperature, min_humidity, max_humidity

  # read a function and split the return values into four variables
  min_temperature, max_temperature, min_humidity, max_humidity = read_json(file_name)

  conn=sqlite3.connect(dbname)
  curs=conn.cursor()
  for row in curs.execute("SELECT * FROM SENSEHAT_data"):
      row_l = list(row)
      print(row_l)
      if (row_l[1] > max_temperature or row_l[1] < min_temperature) or (row_l[2] > max_humidity or row_l[2] < min_humidity):
        print('The temperature or the humidity is out of the range\
          Temperature range is (', min_temperature, '-', max_temperature, ')\
            Humidity range is (', min_humidity, '-', max_humidity, ')')
      else:
        print(row_l)
  conn.close()



# call methods
create_table(dbname)
logData(dbname, measure_temp_hum)
# displayData(dbname)
check_temp_hum(dbname, 'config.json')