import unittest
import matplotlib.pyplot as plt
import numpy as np
import S2F
import utilities


class TestDataHelper(unittest.TestCase):

    def test_getBTCdata(self):
        print(S2F.S2FvsMarketValue.getBTCPrice())

    def test_calculateStock(self):
        df = S2F.S2FvsMarketValue.calculateStock()
        plt.plot(df["Date"], df["Stock"])
        plt.show()

    def test_calculateMarketValue(self):
        stock = S2F.S2FvsMarketValue.calculateStock()
        price = S2F.S2FvsMarketValue.getBTCPrice()
        return S2F.S2FvsMarketValue.calculateMarketValue(stock, price)

    def test_hypotheticalS2F(self):
        return S2F.S2FvsMarketValue.calculateHypotheticalS2F()

    def test_S2FModel(self):
        s2f = self.test_hypotheticalS2F()
        mv = self.test_calculateMarketValue()
        df = S2F.S2FvsMarketValue.merge_S2FandMarketValue(s2f, mv)
        df = utilities.DataFrameOperations.convertDailyDataToMonthlyData(df)
        S2F.S2FvsMarketValue.S2FModel(df)