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
  # conn.commit()
  # close the connection
  # conn.close()


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

  for sensehat_row_l in curs.execute("SELECT * FROM SENSEHAT_data"):
      # curr_date = list(sensehat_row_l.split()[0])
      print(sensehat_row_l)
      notification_data = curs.execute("SELECT COUNT(*) FROM NOTIFICATION_data")
      print(notification_data)

      # for row_in_noification in curs.execute("SELECT * FROM NOTIFICATION_data"):
      #     print(row_in_noification)
      #     print('row_in_noification is printing')
      #     break
      #     notification_row_l = list(row_in_noification)
      #     print(notification_row_l)
      #     notification_date = notification_row_l[0].split()[0]
      #     if curr_date == notification_date:
      #       print('date is in the notification table')
      #       break

      #     else:
      #       if ((sensehat_row_l[1] > min_temperature) and (sensehat_row_l[1] < max_temperature)) and ((sensehat_row_l[2] > min_humidity) and (sensehat_row_l[2] < max_humidity)):
      #         print(sensehat_row_l)
      #       else:
      #         # send notification
      #         print('out of range')
      #         execute_notification()
      #           # insert data into the table
      #         curs.execute("INSERT INTO NOTIFICATION_data values(?)", (notification_date))

  # conn.close()



# display database data
def displayData():
    conn=sqlite3.connect(dbname)
    curs=conn.cursor()
    print ("\nEntire database contents:\n")
    for row in curs.execute("SELECT DISTINCT timestamp FROM SenseHat_data"):
        print (row)
    # conn.close()



ACCESS_TOKEN="o.w75BDnf5ujJdrsQ15ZcjFB3je03NEn3C"

def send_notification_via_pushbullet(title, body):
    """ Sending notification via pushbullet.
        Args:
            title (str) : title of text.
            body (str) : Body of text.
    """
    data_send = {"type": "note", "title": title, "body": body}
 
    resp = requests.post('https://api.pushbullet.com/v2/pushes', data=json.dumps(data_send),
                         headers={'Authorization': 'Bearer ' + ACCESS_TOKEN, 
                         'Content-Type': 'application/json'})
    if resp.status_code != 200:
        raise Exception('Something wrong')
    else:
        print('complete sending')

def execute_notification():
  ip_address = os.popen('hostname -I').read()
  send_notification_via_pushbullet(ip_address, "The temperature or the humidity is out of the range")


# call methods
logData(dbname, measure_temp_hum)
# displayData(dbname)
check_temp_hum(dbname, 'config.json')
# displayData()