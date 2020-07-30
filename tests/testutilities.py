import math

import pandas as pd
import unittest

import utilities

class TestPandas(unittest.TestCase):

    def test_dataframe_concat(self):
        df1 = TestHelper.createTestDataFrame()
        df2 = TestHelper.createSecondDataFrame()
        result = pd.concat([df1, df2], axis=1, sort=False)
        self.assertEqual(len(result.columns), 4)

    def test_drop_non_numerical(self):
        df = TestHelper.createDataFrameWithDates()
        self.assertEqual(len(df.columns), 3)
        df = df.select_dtypes(['number'])
        self.assertEqual(len(df.columns), 2)
        print(df)
        self.assertEqual(df.columns[0], "value1")
        self.assertEqual(df.columns[1], "value2")

class TestJsonExporter(unittest.TestCase):

    def test_pandastojson(self):
        df = TestHelper.createTestDataFrame()
        folder = "tests"
        filename = "/testJson.json"
        utilities.JsonConverter.exportDataFrameToJson(df, folder, filename)

    def test_jsontopandas(self):
        folder = "tests"
        filename = "/testJson.json"
        df = utilities.JsonConverter.jsonToDataFrame(folder, filename)
        self.assertTrue(isinstance(df, pd.DataFrame))

class TestDescriptiveStatistics(unittest.TestCase):

    def test_pct_change(self):
        a = 30
        b = 40
        c = 60
        data = [["2020-01-01", a],
                ["2020-01-02", b],
                ["2020-01-03", c]]

        df = pd.DataFrame(data)
        df = utilities.DescriptiveStatistics.calcualatePctChange(df._get_numeric_data())
        self.assertTrue(math.isnan(df.at[0, 1]))
        self.assertAlmostEqual(df.at[1, 1], (b - a) / a)
        self.assertAlmostEqual(df.at[2, 1], (c - b) / b)

    def test_show_histogram(self):
        x = [21, 22, 23, 4, 5, 6, 77, 8, 9, 10, 31, 32, 33, 34, 35, 36, 37, 18, 49, 50, 100]
        df = pd.DataFrame(x)
        df.columns = ["values"]
        utilities.DescriptiveStatistics.showHistogram(df)

    def test_show_plot(self):
        df = TestHelper.createTestDataFrame()

        column_names = ['value1', 'value2']
        utilities.DescriptiveStatistics.showPlots(df, column_names)
    def test_scatterplotmatrix(self):
        df = TestHelper.createTestDataFrame()

        utilities.DescriptiveStatistics.showScatterPlotMatrix(df)

    def test_summary_of_descriptive_statistics(self):
        df = TestHelper.createTestDataFrame()

        utilities.DescriptiveStatistics.summaryDescriptiveStatistics(df)

class TestHelper:

    @staticmethod
    def createTestDataFrame():
        data = {'value1': [21, 22, 23, 4, 5, 6, 77, 8, 9, 10, 31, 32, 33, 34, 35, 36, 37, 18, 49, 50, 100],
                'value2': [23, 56, 23, 67, 5, 23, 7, 83, 94, 130, 21, 32, 33, 34, 45, 36, 37, 28, 43, 59, 109]
                }
        df = pd.DataFrame(data, columns=['value1', 'value2'])
        return df

    @staticmethod
    def createSecondDataFrame():
        data = {'value3': [21, 22, 23, 4, 5, 6, 77, 8, 9, 10, 31, 32, 33, 34, 35, 36, 37, 18, 49, 50, 100],
                'value4': [23, 56, 23, 67, 5, 23, 7, 83, 94, 130, 21, 32, 33, 34, 45, 36, 37, 28, 43, 59, 109]
                }
        df = pd.DataFrame(data, columns=['value3', 'value4'])
        return df

    @staticmethod
    def createDataFrameWithDates():
        data = {'date': ["2020-01-01", "2020-01-02", "2020-01-03"],
                'value1': [21, 22, 23],
                'value2': [23, 56, 23]
                }
        df = pd.DataFrame(data, columns=['date', 'value1', 'value2'])
        return df

