# import packages
import sqlite3

# initialize databse name
dbname = 'sensehat.db'

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

create_table(dbname)