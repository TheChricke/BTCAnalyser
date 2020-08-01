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

    def __init__(self, commodity):
        self.COMMODITY = commodity

    # fetches historical prices for gold from Investing.com
    # returns a pandas dataframe
    def fetchData(self):
        df = investpy.get_commodity_historical_data(commodity=self.COMMODITY,
                                                    from_date=Constants.start_date.strftime("%D/%M/%Y"),
                                                    to_date=Constants.end_date.strftime("%D/%M/%Y"))
        return df


class GoogleTrendsData(ApiFetcher):

    def __init__(self, searchwords):
        self.SEARCH_WORDS = searchwords

    # fetches historical data for amount of google searches for a certain word
    def fetchData(self):
        pytrend = TrendReq(hl='en-GB', tz=360)
        dataset = []
        start_date_str = Constants.start_date.strftime("%Y-%M-%D")
        end_date_str = Constants.end_date.strftime("%Y-%M-%D")
        for x in range(0, len(self.SEARCH_WORDS)):
            keywords = [self.SEARCH_WORDS[x]]
            pytrend.build_payload(
                kw_list=keywords,
                cat=0,
                timeframe=start_date_str + ' ' + end_date_str,
                geo='GB')
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
            date_string = self.utcToDate(data["timestamp"]).strftime('%Y-%m-%d')
            row = [date_string, S2F]
            data_array.append(row)

        return pd.DataFrame(data_array, columns=["date", "S2F"])

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

    # Imports data from a number of online sources.
    #
    # Currently supports Google Finance, St.Louis FED(FRED), and Kenneth French 's data library, among others.
    def fetchData(self):
        SnP500 = web.DataReader(['sp500'], 'fred', Constants.start_date, Constants.end_date)
        return SnP500
