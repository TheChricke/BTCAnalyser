import abc
import pandas as pd
import investpy
import requests
from datetime import datetime
import pandas_datareader.data as web
from pytrends.request import TrendReq

import Constants


class ApiFetcher(metaclass=abc.ABCMeta):

    def __init__(self, baseUrl, path, parameters, headers):
        self.baseurl = baseUrl
        self.path = path
        self.parameters = parameters
        self.headers = headers

    @abc.abstractmethod
    def fetchData(self):
        pass


class CommodityPriceData(ApiFetcher):

    def __init__(self, baseUrl, path, parameters, headers, commodity):
        super().__init__(baseUrl, path, parameters, headers)
        self.COMMODITY = commodity

    # fetches historical prices for gold from Investing.com
    # returns a pandas dataframe
    def fetchData(self):
        df = investpy.get_commodity_historical_data(commodity=self.COMMODITY,
                                                    from_date=Constants.start_date.strftime("%D/%M/%Y"),
                                                    to_date=Constants.end_date.strftime("%D/%M/%Y"))
        return df


class GoogleTrendsData(ApiFetcher):

    def __init__(self, baseUrl, path, parameters, headers, searchwords):
        super().__init__(baseUrl, path, parameters, headers)
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

    def __init__(self, baseUrl, path, parameters, headers):
        super().__init__(baseUrl, path, parameters, headers)
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
        return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d')

    def calculateBlockHeightAtEndDate(self):
        pass

    def fetchData(self):
        data = []

        blocks_per_day = self.calculateBlocksPerDay()

        blockNr = 1
        while True:
            r = requests.get(Constants.CHAIN_API_URL + "/block/" + blockNr,
                         headers=self.HEADERS)
            response = r.json()
            error_no = response["error_no"]
            if error_no == 1: #we have reached the end of the blockchain
                break
            blockNr = blockNr + blocks_per_day
            block_reward = response["data"]["reward_block"]
            S2F = self.totalBTC / self.calculateNewBTCForYear(block_reward, blocks_per_day)
            date = self.utcToDate(response["data"]["timestamp"])
            row = [date, S2F]
            data.append(row)

        return pd.DataFrame(data, columns=["date", "S2F"])


class SnP500Data(ApiFetcher):

    def __init__(self, baseUrl, path, parameters, headers):
        super().__init__(baseUrl, path, parameters, headers)
        self.HEADERS = headers

    # Imports data from a number of online sources.
    #
    # Currently supports Google Finance, St.Louis FED(FRED), and Kenneth French 's data library, among others.
    def fetchData(self):
        SnP500 = web.DataReader(['sp500'], 'fred', Constants.start_date, Constants.end_date)
        return SnP500

# TODO pass paths and constants to init instead
