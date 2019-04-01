# import packages
import sqlite3

# initialize databse name
dbname = 'sensehat.db'

# this method creates a table for the notification to store the date 
def create_table(dbname):
  # make a connection and create a database if doesn't exist
  conn = sqlite3.connect(dbname)
  with conn: 
      # set up the cursor
      cur = conn.cursor() 
      # drop table if any exists
      cur.execute("DROP TABLE IF EXISTS NOTIFICATION_data")
      # create a table to store the date whenveer we send a notification
      # also, check if the date is in the table
      cur.execute("CREATE TABLE NOTIFICATION_data(Date TEXT, type TEXT)")
  # commit changes
  conn.commit()
  # close the connection
  conn.close()

create_table(dbname)