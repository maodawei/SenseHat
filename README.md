# IOT application by Mohammed Alotaibi & Dawei Mao

In this project, we developed an Internet of Things small application where we used python as the main language to develop the project and Raspberry pi as the hardware.

At first, we have a JSON config file will store a temperature and humidity range. This file should be called config.json. 

Second, We also created a python file called monitorAndNotify.py which will log the current time, temperature and humidity to an sqlite3 database every minute. After saving to the database, we checked if either the temperature or humidity are outside the configured range and if so, push a notification using Pushbullet. Only send a maximum of 1 notification per day, i.e., don’t resend the notification every minute. We achieved this by using the database to remember if we've already sent a notification today.

Third, we created a python file called createReport.py which will create two csv files called report.csv and plot_data.csv. The report.csv file would contain a separate row for each days’ data, additionally this data resides in the database. If each piece of data is within the configured temperature and humidity range, then the status of OK is applied, otherwise the label of BAD is applied. An appropriate message detailing the error(s) is included. The plot_data.csv file would contain a separate row for each days, data of minimum temperature and humidity and maximum temperature and humidity which then will be used for analysis purpose.

Fourth, we created a python file called bluetooth.py using Bluetooth to detect nearby devices and when connected send an appropriate message stating the current temperature, humidity and if these fall within the configured temperature and humidity range.

Finally, we used 2 different Python data visualisation libraries 'pandas, and matplotlib' to create 2 images(png files). We used plot_data.csv file to read the data into a python pandas data frame, then create two plots which shows the minimum and maximum temperature and humidity for each day. We used pandas line graph and matplotlib scatter plot.
