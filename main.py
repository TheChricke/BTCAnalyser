from data import DataWrapper
from api import ApiFetcher

BLOCKCYPHER_BASE_URL = "https://api.blockcypher.com/v1/btc/main"
BLOCKCHAIN_INFO_BASE_URL = "https://blockchain.info"

dataWrapper = DataWrapper()
apiFetcher = ApiFetcher(BLOCKCYPHER_BASE_URL, "/blocks/1?txstart=1&limit=1", None)
print(apiFetcher.fetchData())
