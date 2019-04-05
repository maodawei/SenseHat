# import packages
import pandas as pd
import matplotlib.pyplot as plt
# import seaborn as sns
from db import database

class anaytics:

    @staticmethod
    def plot_day_data_graph():
        # call the getEnvironmentData from database class and assigne the desired values to a variable
        list_of_rows, _, _ = database.getEnvironmentData()
        # create a pandas dataframe
        df = pd.DataFrame(list_of_rows, columns=['date', 'temperature', 'humidity'])
        df.set_index(['date'], inplace=True)
        df = pd.to_datetime(df)
        # print(df.loc['2019-04-03'])
        df['humidity'].plot()
        #plt.plot(df)
        plt.title('The title with font size: 20, and font:monospace')
        plt.xlabel('xlabel')
        plt.ylabel('ylabel')
        plt.savefig('plot_day_data_graph.png')
        plt.show()

    @staticmethod
    def plot_daily_graph(file_name):
        # load the csv file into a pandas dataframe
        df = pd.read_csv(file_name)
        df.set_index(['Date'], inplace=True)
        print(df)
        # df.plot()
        # plt.title('The title with font size: 20, and font:monospace')
        # plt.xlabel('xlabel')
        # plt.ylabel('ylabel')
        # plt.savefig('plot_daily_graph.pig')

anaytics.plot_day_data_graph()
# anaytics.plot_daily_graph('report.csv')