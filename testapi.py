import datetime
import json
import unittest

import requests
import pandas as pd

import Constants
import api

class TestApi(unittest.TestCase):

    def test_get_request(self):
        url = "https://jsonplaceholder.typicode.com/todos/1"
        r = requests.get(url)
        response = r.json()
        value = response["id"]
        print(value)

    def test_init_and_append_dataframe(self):
        data = []
        data.append(["2020-01-01", 35])
        data.append(["2020-01-02", 35])
        df = pd.DataFrame(data, columns=["date", "value"])
        print(df)

class TestBlockRewards(unittest.TestCase):

    def test_blocks_perday(self):
        blockreward = api.BlockRewardData(None, None, None)
        blocksPerDay = blockreward.calculateBlocksPerDay()
        self.assertEqual(blocksPerDay, 144)

    def test_utc_to_date(self):
        timestamp = 1231469665
        blockreward = api.BlockRewardData(None, None, None)
        self.assertEqual(blockreward.utcToDate(timestamp), "2009-01-09")

    def test_compareDateTimes(self):
        date1 = datetime.datetime(2014, 3, 2)
        date2 = datetime.datetime(2013, 8, 1)
        self.assertTrue(date1 > date2)

        timestamp1 = 1231469665
        datetime.datetime.utcfromtimestamp(timestamp1)
        timestamp2 = 1231468665
        datetime.datetime.utcfromtimestamp(timestamp2)
        self.assertTrue(date1 > date2)

    def test_buildBlockRewardDataFrame(self):
        blockreward = api.BlockRewardData(Constants.CHAIN_API_URL, "/block/", Constants.HEADERS_CHAIN_API)
        blocks_per_day = blockreward.calculateBlocksPerDay()
        df = blockreward.buildBlockRewardDataFrame(datetime.datetime(2009, 2, 11), blocks_per_day)
        print(df)
