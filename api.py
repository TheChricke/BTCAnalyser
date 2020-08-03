import abc
from time import sleep

import pandas as pd
import investpy
import requests
from datetime import datetime
import pandas_datareader.data as web
from pytrends.request import TrendReq

import Constants


class ApiFetcher(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def fetchData(self):
        pass


class CommodityPriceData(ApiFetcher):

    def __init__(self, commodity, start_date, end_date):
        self.COMMODITY = commodity
        self.start_date = start_date
        self.end_date = end_date

    # fetches historical prices for gold from Investing.com
    # returns a pandas dataframe
    def fetchData(self):
        df = investpy.get_commodity_historical_data(commodity=self.COMMODITY,
                                                    from_date=self.start_date.strftime("%d/%m/%Y"),
                                                    to_date=self.end_date.strftime("%d/%m/%Y"))
        df = df.reset_index()
        df = df[["Date", "Close"]]
        return df


class GoogleTrendsData(ApiFetcher):

    def __init__(self, searchwords, start_date, end_date):
        self.SEARCH_WORDS = searchwords
        self.start_date = start_date
        self.end_date = end_date

    # fetches historical data for amount of google searches for a certain word
    def fetchData(self):
        pytrend = TrendReq(hl='en-GB', tz=360, timeout=(10,25), proxies=['https://34.203.233.13:80',], retries=2, backoff_factor=0.1)
        dataset = []
        start_date_str = self.start_date.strftime("%Y-%M-%D")
        end_date_str = self.end_date.strftime("%Y-%M-%D")
        for x in range(0, len(self.SEARCH_WORDS)):
            keywords = [self.SEARCH_WORDS[x]]
            pytrend.build_payload(
                kw_list=keywords,
                cat=0,
                timeframe=start_date_str + ' ' + end_date_str)
            data = pytrend.interest_over_time()
            if not data.empty:
                data = data.drop(labels=['isPartial'], axis='columns')
                dataset.append(data)
        result = pd.concat(dataset, axis=1)
        return result


class BlockRewardData(ApiFetcher):

    def __init__(self, baseUrl, path, headers):
        self.baseUrl = baseUrl
        self.path = path
        self.HEADERS = headers
        self.totalBTC = 0

    def calculateBlocksPerDay(self):
        interval = 10
        minutesPerDay = 60*24
        blocksPerDay = minutesPerDay/interval
        return blocksPerDay

    def calculateNewBTCForYear(self, blockreward, blocksPerDay):
        return blockreward*blocksPerDay*365

    def utcToDate(self, timestamp):
        return datetime.utcfromtimestamp(int(timestamp))

    def fetchData(self):
        return self.buildBlockRewardDataFrame(Constants.end_date, self.calculateBlocksPerDay())

    def buildBlockRewardDataFrame(self, end_date, blocks_per_day):
        data_array = []

        blockNr = 1
        while True:
            response = self.fetchBlock(blockNr)
            data = response['data']
            timestamp = data['timestamp']
            date = self.utcToDate(timestamp)
            if date > end_date:  # we have reached passed the end date
                break
            blockNr = int(blockNr + blocks_per_day)
            block_reward = self.getBlockReward(response)
            self.totalBTC = self.totalBTC + block_reward*blocks_per_day
            S2F = self.calcualteS2F(self.totalBTC, block_reward, blocks_per_day)
            row = self.buildRowData(response, S2F)
            data_array.append(row)

        return pd.DataFrame(data_array, columns=["Date", "S2F"])

    def buildRowData(self, response, S2F):
        date_string = self.utcToDate(response["data"]["timestamp"]).strftime('%Y-%m-%d')
        return [date_string, S2F]

    def fetchBlock(self, block_height):
        r = requests.get(self.baseUrl + self.path + str(block_height),
                         headers=self.HEADERS)
        response = r.json()
        if response["err_code"] != 0:
            raise Exception("Error fetching data from chain api: " + response["message"]
                            + " url: " + self.baseUrl + self.path + str(block_height))
        return r.json()

    def calcualteS2F(self, totalbtc, block_reward, blocks_per_day):
        return totalbtc / self.calculateNewBTCForYear(block_reward, blocks_per_day)

    def getBlockReward(self, response):
        return response['data']["reward_block"] / 100000000

class SnP500Data(ApiFetcher):

    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date

    # Imports data from a number of online sources.
    #
    # Currently supports Google Finance, St.Louis FED(FRED), and Kenneth French 's data library, among others.
    def fetchData(self):
        df = web.DataReader(['sp500'], 'fred', self.start_date, self.end_date)
        df = df.reset_index()
        df = df[["DATE", "sp500"]]
        df = df.rename(columns={"DATE": "Date", "sp500": "sp500"})
        return df

class CryptoPriceData(ApiFetcher):

    def __init__(self, start_date, end_date, crypto):
        self.start_date = start_date
        self.end_date = end_date
        self.crypto = crypto

    def fetchData(self):
        df = investpy.get_crypto_historical_data(self.crypto,
                                                    from_date=self.start_date.strftime("%d/%m/%Y"),
                                                    to_date=self.end_date.strftime("%d/%m/%Y"))
        return df
