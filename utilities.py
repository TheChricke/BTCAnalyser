import json
import os
import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix
import numpy as np
import pandas as pd


class JsonConverter:

    @staticmethod
    def createFolder(folder):
        if not os.path.exists(folder):
            os.makedirs(folder)

    @staticmethod
    def exportDataFrameToJson(df, folder, file_name):
        JsonConverter.createFolder(folder)
        json = df.to_json()
        print("Writing to path " + folder + file_name)
        f = open(folder + file_name, "w+")
        f.write(json)
        f.close()

    @staticmethod
    def jsonToDataFrame(folder, file_name):
        path = folder + file_name
        jsonStr = ""
        if os.path.exists(path):
            f = open(folder + file_name, "r")
            jsonStr = f.read()
            f.close()

        return pd.read_json(jsonStr)

class DescriptiveStatistics:

    @staticmethod
    def calcualatePctChange(df):
        return df.pct_change()

    @staticmethod
    def showHistogram(df):
        colname = df.columns[0]
        num_bins = 20
        plt.hist(df.to_numpy(), num_bins, facecolor='blue', alpha=0.5)
        plt.ylabel('Probability')
        plt.xlabel(colname)
        plt.title('Histogram of ' + colname)
        plt.show()

    @staticmethod
    def showPlots(df, column_names):
        plt.plot(df.loc[:, column_names])
        plt.legend(column_names)
        plt.show()

    @staticmethod
    def showScatterPlotMatrix(df):
        scatter_matrix(df, alpha = 0.2, figsize = (6, 6), diagonal = 'kde')
        plt.show()

    @staticmethod
    def summaryDescriptiveStatistics(df):
        result = df.describe(include=[np.number])
        return result