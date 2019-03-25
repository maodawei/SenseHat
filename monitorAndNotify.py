# import packages
import sqlite3
from datetime import datetime
# from crontab import CronTab
# from sense_hat import SenseHat
import os
import time

# initialize databse name
dbname = 'databases/sensehat.db'
# get the current time
time = datetime.now().strftime("%H:%M")

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

    print("t=%.1f  t_cpu=%.1f  t_corr=%.1f  h=%d  p=%d" % (t, t_cpu, t_corr, round(h), round(p)))
    # return both termpreature after correction and humidity
    return round(t_corr), round(h)

# log sensor data on database
def logData(dbname, time, measure_temp_hum):
    # extract both termpreature and humidity from the function measure_temp_hum
    temp, hum = measure_temp_hum	
    # make a connection and create a database if doesn't exist
    conn = sqlite3.connect(dbname)
    # set up the cursor
    curs = conn.cursor()
    # insert data into the table
    curs.execute("INSERT INTO SENSEHAT_data values(datetime(time), (temp), (hum))", (time, temp,hum))
    # commit changes
    conn.commit()
    # close the connection
    conn.close()

# call the method
create_table(dbname)
logData(dbname, time, measure_temp_hum)