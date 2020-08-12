import pandas as pd
import matplotlib.pyplot as plt

class DataCleaning:

    @staticmethod
    def remove_empty_rows(df):
        return df.dropna()

class Analytics:

    @staticmethod
    def checkForRandomData(dataset):
        fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(10, 6))
        dataset.plot(ax=ax1)
        pd.plotting.lag_plot(dataset)
        plt.show()