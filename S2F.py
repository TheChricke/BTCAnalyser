import datetime

import Constants
import api
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import utilities


class S2FvsMarketValue:

    @staticmethod
    def calculateHypotheticalS2F():
        date = datetime.datetime(2009, 1, 9)
        end_date = Constants.end_date
        block_height = 0
        current_reward = 50
        blocks_per_day = 144
        data_array = []
        stock = 0
        halving_count = 0
        while date < end_date:
            if block_height % 210000 < 144 & block_height != 0:
                current_reward = current_reward / 2
                halving_count = halving_count + 1
            block_height = block_height + blocks_per_day
            stock = stock + blocks_per_day * current_reward
            date += datetime.timedelta(days=1)
            flow = blocks_per_day * current_reward * 365
            data_array.append([date, stock/flow, halving_count])
        df = pd.DataFrame(data_array)
        df = df.rename(columns={0: "Date", 1: "S2F", 2: "Halving"})
        return df

    @staticmethod
    def getBTCPrice():
        btc = api.CryptoPriceData(Constants.start_date, Constants.end_date, "bitcoin")
        df = btc.fetchData()
        df = df.reset_index()[["Date", "Close"]]
        return df

    @staticmethod
    def calculateStock():
        date = Constants.start_date
        end_date = Constants.end_date
        block_height = 0
        current_reward = 50
        blocks_per_day = 144
        data_array = []
        stock = 0
        while date < end_date:
            if block_height % 210000 < 144 & block_height != 0:
                current_reward = current_reward / 2
            block_height = block_height + blocks_per_day
            stock = stock + blocks_per_day * current_reward
            date += datetime.timedelta(days=1)
            data_array.append([date, stock])
        df = pd.DataFrame(data_array)
        df = df.rename(columns={0: "Date", 1: "Stock"})
        return df

    @staticmethod
    def calculateMarketValue(stock, price):
        df = utilities.DataFrameOperations.merge_dataframes([stock, price], 'Date')
        df['MarketValue'] = df.apply(lambda row: row["Close"]*row["Stock"], axis=1)
        df['MarketValue'] = np.log(df['MarketValue'])
        return df

    @staticmethod
    def merge_S2FandMarketValue(s2f, mv):
        return utilities.DataFrameOperations.merge_dataframes([s2f, mv], "Date")

    @staticmethod
    def S2FXModel(df):
        pass

    @staticmethod
    def S2FModel(df):
        fig, ax = plt.subplots()
        colors = {0: 'red', 1: 'blue', 2: 'green'}
        ax.scatter(np.log(df[["S2F"]]), df[["MarketValue"]], c=df['Halving'].apply(lambda x: colors[round(x)]))
        plt.title('Scatter plot')
        plt.xlabel('S2F')
        plt.ylabel('MarketValue')
        plt.show()