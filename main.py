import api
import utilities
import pandas as pd

JSON_OUTPUT_FOLDER = "json_output"

SEARCHWORDS = ["Bitcoin"]
COMMODITY = "gold"
#headers to get chain api working, all the headers copied from the web browser where it worked
HEADERS_CHAIN_API = {"authority": "chain.api.btc.com",
                                  "method": "GET",
                                  "path": "/v3/block/1",
                                  "scheme": "https",
                                  "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                                  "accept-encoding": "gzip, deflate, br",
                                  "accept-language": "sv-SE,sv;q=0.9,en-US;q=0.8,en;q=0.7",
                                  "cache-control": "max-age=0",
                                  "cookie": "_ga=GA1.2.1807831528.1595711050; _gid=GA1.2.2015397938.1595711050; _globalGA=GA1.2.1867564273.1595711050; _globalGA_gid=GA1.2.969215753.1595711050; acw_tc=0bc1a14415957114995183812e5f67fdbb5327a142bc3f3ef9229cf4632ef8",
                                  "sec-fetch-dest": "document",
                                  "sec-fetch-mode": "navigate",
                                  "sec-fetch-site": "none",
                                  "sec-fetch-user": "?1",
                                  "upgrade-insecure-requests": "1",
                                  "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36})"}


goldpricedata = api.CommodityPriceData()
goldprices = goldpricedata.fetchData()
utilities.JsonConverter.exportDataFrameToJson(JSON_OUTPUT_FOLDER, "/goldprice")

googletrendsdata = api.GoogleTrendsData()
googletrends = googletrendsdata.fetchData()
utilities.JsonConverter.exportDataFrameToJson(JSON_OUTPUT_FOLDER, "/googletrends")

blockrewarddata = api.BlockRewardData(HEADERS_CHAIN_API)
blockrewards = blockrewarddata.fetchData()
utilities.JsonConverter.exportDataFrameToJson(JSON_OUTPUT_FOLDER, "/blockreward")

sandp500data = api.SnP500Data()
sandp500 = sandp500data.fetchData()
utilities.JsonConverter.exportDataFrameToJson(JSON_OUTPUT_FOLDER, "/SnP500")

#concatenate data frames and remove non numerical columns(date)
data = pd.concat([goldprices, googletrends, blockrewards, sandp500], axis=1, sort=False).select_dtypes(['number'])
