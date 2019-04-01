# import packages
from datetime import datetime
import sqlite3
import time
# initialize databse name
dbname = 'sensehat.db'

class database:
    @staticmethod
    def create_tables():
        # make a connection and create a database if doesn't exist
        #conn = sqlite3.connect(dbname)
        conn=database.connection()
        with conn: 
            # set up the cursor
            cur = conn.cursor() 
            # drop table if any exists
            cur.execute("DROP TABLE IF EXISTS SENSEHAT_data")
            # create a table to store current time, temperature, humidity
            cur.execute("CREATE TABLE SENSEHAT_data(timestamp DATETIME, temp NUMERIC, hum NUMERIC)")
            cur.execute("DROP TABLE IF EXISTS NOTIFICATION_data")
            # create a table to store the date whenveer we send a notification
            # also, check if the date is in the table
            cur.execute("CREATE TABLE NOTIFICATION_data(Date TEXT, type TEXT)")

        # log sensor data on database
    @staticmethod
    def logData(dbname, measure_temp_hum):
        # extract both termpreature and humidity from the function measure_temp_hum
        temp, hum = measure_temp_hum()
        # make a connection and create a database if doesn't exist
        conn = sqlite3.connect(dbname)
        # set up the cursor
        curs = conn.cursor()
        # insert data into the table
        curs.execute("INSERT INTO SENSEHAT_data values(datetime('now'), ?, ?)", (temp, hum))
        # commit changes
        conn.commit()
        # close the connection
        conn.close()   
    
    @staticmethod
    def connection():
        conn = sqlite3.connect(dbname)

        return conn
    @staticmethod
    def insertEnvironmentData(temp,hum):
        conn=database.connection()
        with conn:
            curs=conn.cursor()
            curs.execute("INSERT INTO SENSEHAT_data values(datetime('now'),?,?)",(temp,hum))
    
    @staticmethod
    def getEnvironmentData():
        conn=database.connection()
        with conn:
            curs=conn.cursor()
            return curs.execute("SELECT * FROM SENSEHAT_date")
    
    @staticmethod
    def getNotificationTimes():
        conn=database.connection()
        with conn:
            curs=conn.cursor()
            for row in curs.execute("SELECT * FROM SENSEHAT_data"):
                curr_date=row.split()[0]
                for row in curs.execute("SELECT * FROM NOTIFICATION_data"):
                    notification_date=row.split()[0]
                    if curr_date == notification_date:
                        return 1
                    else:
                        return 0
    
    @staticmethod
    def insertNotificationTime():
        conn=database.connection()
        with conn:
            curs=conn.cursor()
            curs.execute("INSERT INTO NOTIFICATION_date values(datetime('now'))")        

database.create_tables()