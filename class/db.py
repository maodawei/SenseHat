# import packages
from datetime import date
import sqlite3
import time

# initialize databse name
dbname = 'sensehat.db'

# class database
class database:

    @staticmethod
    def create_tables():
        """
        This function does drop tables in the database if exists.
        Then create two tables named: SENSEHAT_data, NOTIFICATION_data
        """
        # make a connection and create a database if doesn't exist
        conn=database.connection()
        with conn: 
            # set up the cursor
            cur = conn.cursor() 
            # drop table if any exists
            cur.execute("DROP TABLE IF EXISTS SENSEHAT_data")
            # create a table to store current time, temperature, humidity
            cur.execute("CREATE TABLE SENSEHAT_data(timestamp DATETIME, temp NUMERIC, hum NUMERIC)")
            # drop table if any exists
            cur.execute("DROP TABLE IF EXISTS NOTIFICATION_data")
            # create a table to store the date whenveer we send a notification
            # also, check if the date is in the table
            cur.execute("CREATE TABLE NOTIFICATION_data(date TEXT)")
            # drop table if any exists
            cur.execute("DROP TABLE IF EXISTS BLUETOOTH_notification")
            # create a table to store the date whenveer we send a notification
            # also, check if the date is in the table
            cur.execute("CREATE TABLE BLUETOOTH_notification(date TEXT)")

    
    # this function connects to the database and return the connection
    @staticmethod
    def connection(): 
        # connect to the database
        conn = sqlite3.connect(dbname)
        # return connection
        return conn

    @staticmethod 
    # this function inserts temperature and humidity into a table
    def insertEnvironmentData(temp, hum):
        # call the connection function and assign it to a variable
        conn=database.connection()
        with conn:
            # set the cursor
            curs=conn.cursor()
            # insert data into the specified table
            curs.execute("INSERT INTO SENSEHAT_data values(datetime('now'),?,?)",(temp,hum))
    
    # This function retrieve the last inserted data into SENSEHAT_data
    # It returns both temperature and humidity
    @staticmethod
    def getEnvironmentData():
        # connect to the database
        conn=database.connection()
        with conn:
            # set the cursor
            curs=conn.cursor()
            # assign the the table's data into a variable named list_of_rows
            # after converting the sqlite object into a python list
            list_of_rows = list(curs.execute("SELECT * FROM SENSEHAT_data"))
            # assign the tmeperature of the last row to a variable named temp
            temp = list_of_rows[-1][-2]
            # assign the humidity of the last row to a variable named hum
            hum = list_of_rows[-1][-1]

            # return both tmeperature and humidity
            return list_of_rows, temp, hum
    
    @staticmethod
    def getNotificationTimes():
        """
        This function does the following:
        it checks the last date in the inserted in the notification table
        with the current date. If the date is already there, that means we
        already sent a notification today and returns 1. If the table is either
        empty 'which means we have not sent anyting yet' or if the date is not in
        the table, which means we have not sent a notification today, then return 0
        """
        # connect to the database
        conn=database.connection()
        with conn:
            # set up the cursor
            curs=conn.cursor()
            # check if there table is empty
            if not list(curs.execute("SELECT * FROM NOTIFICATION_data")):
                # return 0 if there table is empty
                return 1
            # the table has data
            else:
                # assign the data from the notification table to a variable named last_row
                # after converting it from a sqlite3 object to a python list
                last_row = list(curs.execute("SELECT * FROM NOTIFICATION_data"))
                # assign the last added date to a variable named last_time
                last_time = last_row[-1][0]
                # get today's date 
                today_date = str(date.today())
                # compare the last added date to the notification table
                # to today's date. If they are not equal, than that means
                # the currnent date is not in the table and we have not
                # sent notification today
                if today_date != last_time:
                    # return 1
                    return 1
                # else: we have sent notification today 
                else:
                    # return 0
                    return 0
    
    # this function insert current date to the notification table
    # @staticmethod
    # def insertIntoTable(tableName):
    #     # connect to the database
    #     conn=database.connection()
    #     # get today's date 
    #     today_date = str(date.today())
    #     with conn:
    #         # set up the cursor
    #         curs=conn.cursor()
    #         # insert today's date to the notification table
    #         curs.execute("INSERT INTO {} values(?)", (today_date,))



    # this function insert current date to the notification table
    @staticmethod
    def insertNotificationTime():
        # connect to the database
        conn=database.connection()
        # get today's date 
        today_date = str(date.today())
        with conn:
            # set up the cursor
            curs=conn.cursor()
            # insert today's date to the notification table
            curs.execute("INSERT INTO NOTIFICATION_data values(?)", (today_date,))
    
    @staticmethod
    def insertBluetoothNotificationTime():
        # connect to the database
        conn=database.connection()
        # get today's date 
        today_date = str(date.today())
        with conn:
            # set up the cursor
            curs=conn.cursor()
            # insert today's date to the notification table
            curs.execute("INSERT INTO BLUETOOTH_notification values(?)", (today_date,))
    
    @staticmethod
    def getBluetoothNotificationTimes():
        # connect to the database
        conn=database.connection()
        with conn:
            # set up the cursor
            curs=conn.cursor()
            # check if there table is empty
            if not list(curs.execute("SELECT * FROM BLUETOOTH_notification")):
                # return 0 if there table is empty
                return 1
            # the table has data
            else:
                # assign the data from the notification table to a variable named last_row
                # after converting it from a sqlite3 object to a python list
                last_row = list(curs.execute("SELECT * FROM BLUETOOTH_notification"))
                # assign the last added date to a variable named last_time
                last_time = last_row[-1][0]
                # get today's date 
                today_date = str(date.today())
                # compare the last added date to the notification table
                # to today's date. If they are not equal, than that means
                # the currnent date is not in the table and we have not
                # sent notification today
                if today_date != last_time:
                    # return 1
                    return 1
                # else: we have sent notification today 
                else:
                    # return 0
                    return 0