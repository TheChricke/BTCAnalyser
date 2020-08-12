import unittest
import pandas as pd

import Constants
import dataanalytics
import utilities


class TestHelper:

    @staticmethod
    def createTestData():
        df = {"row1" : [1,2,3,4, None],
              "row2" : [2,4,2,3, None]}
        return pd.DataFrame(df)


class TestDataCleaning(unittest.TestCase):

    def read_csv_file(self, path, filename):
        return pd.read_csv(path + filename)

    def create_test_DF(self):
        df = utilities.DataFrameOperations.merge_dataframes([
            self.read_csv_file(Constants.TEST_DATA_FOLDER, "/BTC-USD.csv")[["Date", "Close"]],
            self.read_csv_file(Constants.TEST_DATA_FOLDER, "/Gold.csv")[["Date", "Close"]],
            self.read_csv_file(Constants.TEST_DATA_FOLDER, "/GSPC.csv")[["Date", "Close"]]])
        print(df.info())
        return df[["Close_x", "Close_y", "Close"]]

    def test_remove_non_numerical_rows(self):
        df = self.read_csv_file(Constants.TEST_DATA_FOLDER, "/BTC-USD.csv")
        df = TestHelper.createTestData()
        df = dataanalytics.DataCleaning.remove_empty_rows(df)
        print(df)

    def test_checkForRandomData(self):
        df = self.create_test_DF()
        print(df.info())
        dataanalytics.Analytics.checkForRandomData(dataanalytics.DataCleaning.remove_empty_rows(df))


