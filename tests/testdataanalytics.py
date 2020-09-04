import unittest
import pandas as pd

import Constants
import dataanalytics
import utilities


class TestHelper:

    @staticmethod
    def read_csv_file(path, filename):
        return pd.read_csv(path + filename)

    @staticmethod
    def createTestData():
        df = {"col1" : [1,2,3,4,2,3,6,5,3,8,3,8,9,5,8, None],
              "col2" : [2,4,2,3,3,2,5,4,3,2,6,4,7,2,3, None],
              }
        return pd.DataFrame(df)

    @staticmethod
    def create_test_DF():
        df = utilities.DataFrameOperations.merge_dataframes([
            TestHelper.read_csv_file(Constants.TEST_DATA_FOLDER, "/BTC-USD.csv")[["Date", "Close"]],
            TestHelper.read_csv_file(Constants.TEST_DATA_FOLDER, "/Gold.csv")[["Date", "Close"]],
            TestHelper.read_csv_file(Constants.TEST_DATA_FOLDER, "/SnP.csv")[["Date", "Close"]]], "Date")
        print("********test dataFrame********")
        print(df.info())
        return df[["Close_x", "Close_y", "Close"]]

class TestDataCleaning(unittest.TestCase):

    def test_remove_non_numerical_rows(self):
        df = TestHelper.read_csv_file(Constants.TEST_DATA_FOLDER, "/BTC-USD.csv")
        df = TestHelper.createTestData()
        df = dataanalytics.DataCleaning.remove_empty_rows(df)
        print(df)

    #stationarity check
    def test_augmented_dickey_fuller_statistics(self):
        df = TestHelper.create_test_DF()
        col1 = dataanalytics.DataCleaning.remove_empty_rows(df[["Close_x"]])
        dataanalytics.VAR_Builder.augmented_dickey_fuller_statistics(col1)

class TestDataAnalytics(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.df = dataanalytics.DataCleaning.remove_empty_rows(TestHelper.create_test_DF())
        self.VARBuilder = dataanalytics.VAR_Builder(self.df, 3)

    def test_checkForRandomData(self):
        self.VARBuilder.checkForRandomData()

    def test_visualize_dataset(self):
        self.VARBuilder.visualize_dataset()

    def test_augmented_dickey_fuller_statistics(self):
        self.VARBuilder.augmented_dickey_fuller_statistics()

    def test_cointegration_test(self):
        self.VARBuilder.cointegration_test()

    def test_grangers_causation_matrix(self):
        self.VARBuilder.grangers_causation_matrix(1)

    def test_select_order_of_VAR_model(self):
        self.VARBuilder.select_order_of_VAR_model()

    def test_fit_VAR_model_and_check_for_serial_correlation(self):
        fitted_model = self.VARBuilder.fit_VAR_model(4)
        self.VARBuilder.check_for_serial_correlation(fitted_model)




