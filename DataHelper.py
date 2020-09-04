import datetime
import pandas as pd
import Constants
import matplotlib.pyplot as plt


class HypotheticalS2FCalculator:

    @staticmethod
    def calculateHypotheticalS2F():
        date = datetime.datetime(2009, 1, 9)
        end_date = Constants.end_date
        block_height = 0
        current_reward = 50
        blocks_per_day = 144
        data_array = []
        flow = blocks_per_day*current_reward*365
        stock = 0
        while date < end_date:
            if block_height % 210000 < 144 & block_height != 0:
                current_reward = current_reward/2
            block_height = block_height + blocks_per_day
            stock = stock + blocks_per_day*current_reward
            date += datetime.timedelta(days=1)
            data_array.append(stock/flow)
        df = pd.DataFrame(data_array)
        plt.plot(data_array)
        plt.show()