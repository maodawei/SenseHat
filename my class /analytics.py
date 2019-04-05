# import packages
import pandas as pd
import matplotlib.pyplot as plt
# import seaborn as sns
from db import database

class anaytics:

    @staticmethod
    def return_dataframe():
        # create a pandas dataframe
        df = pd.read_csv('plot_data.csv', parse_dates=['date'])
        df.set_index('date', inplace=True)
        # return the dataframe
        return df

    @staticmethod
    def daily_temperature_plot():
        # call the return_dataframe method
        df = anaytics.return_dataframe()
        # set size of the plot
        fig, ax = plt.subplots(figsize=(15,7))
        #plot data
        df.plot(y=['min_temp', 'max_temp'], ax=ax)
        plt.scatter(df.index, df['min_temp'])
        plt.scatter(df.index, df['max_temp'])
        # set title
        plt.title('Temperature for each day')
        # set x label
        plt.xlabel('Date')
        # set y label
        plt.ylabel('Degree')
        # save image
        plt.savefig('daily_temperature_plot.png')
        # show image
        plt.show()

    @staticmethod
    def daily_humidity_plot():
        # call the return_dataframe method
        df = anaytics.return_dataframe()
        # set size of the plot
        fig, ax = plt.subplots(figsize=(15,7))
        #plot data
        df.plot(y=['min_hum', 'max_hum'], ax=ax)
        plt.scatter(df.index, df['min_hum'])
        plt.scatter(df.index, df['max_hum'])
        # set title
        plt.title('Humidity for each day')
        # set x label
        plt.xlabel('Date')
        # set y label
        plt.ylabel('Degree')
        # save image
        plt.savefig('daily_humidity_plot.png')
        # show image
        plt.show()
        # plt.savefig('plot_daily_graph.pig')

# call class functions 
anaytics.daily_temperature_plot()
anaytics.daily_humidity_plot()