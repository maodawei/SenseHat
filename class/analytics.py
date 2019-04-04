# import packages
import pandas as pd
import matplotlib.pyplot as plt
# import seaborn as sns
from db import database

class anaytics:

    @staticmethod
    def store_to_dataframe():
        # call the getEnvironmentData from database class and assigne the desired values to a variable
        list_of_rows, _, _ = database.getEnvironmentData()
        # create a pandas dataframe
        df = pd.DataFrame(list_of_rows, columns=['date', 'temperature', 'humidity'])
        # print()
        # df.plot()
        plt.plot(df)
        plt.savefig('pic.png')
        # plt.show()


anaytics.store_to_dataframe()