from db import database
from environment import temperature

# get the current temperature and humidity from raspberry
temp, hum = temperature.measure_temp_hum()
# insert the data into SENSEHAT_data table
database.insertEnvironmentData(temp, hum)
#check to sent notification or not
temperature.check_temp_hum('config.json')