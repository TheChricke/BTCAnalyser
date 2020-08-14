import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.tsa.stattools as statsmodels


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

    # stationarity check
    def augmented_dickey_fuller_statistics(array):
        result = statsmodels.adfuller(array)

        print('ADF Statistic: %f' % result[0])
        print('p-value: %f' % result[1])
        print('Critical Values:')
        for key, value in result[4].items():
            print('\t%s: %.3f' % (key, value))
