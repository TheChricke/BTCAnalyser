import datetime
import enum


class Run_Mode(enum.Enum):
   ONE_VARIABLE = 1
   SHOW_DESCRIPTIVE = 2
   RUN_REGRESSION = 3

RUN_MODE = [Run_Mode.ONE_VARIABLE, Run_Mode.SHOW_DESCRIPTIVE]

BLOCKCYPHER_BASE_URL = "https://api.blockcypher.com/v1/btc/main"
BLOCKCHAIN_INFO_BASE_URL = "https://blockchain.info"
COINCAP_BASE_URL = "https://api.coincap.io/v2"
QUANDL_API_URL = "https://www.quandl.com/api/v3/"
CHAIN_API_URL = "https://chain.api.btc.com/v3"

START_DATE_YEAR = "2009"
START_DATE_MONTH = "01"
START_DATE_DAY = "09"

END_DATE_YEAR = "2020"
END_DATE_MONTH = "07"
END_DATE_DAY = "27"

start_date = datetime.datetime(int(START_DATE_YEAR), int(START_DATE_MONTH), int(START_DATE_DAY))
end_date = datetime.datetime(int(END_DATE_YEAR), int(END_DATE_MONTH), int(END_DATE_DAY))

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
