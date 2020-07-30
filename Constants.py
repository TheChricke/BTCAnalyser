import datetime

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
