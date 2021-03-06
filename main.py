import enum

import Constants
import api
import utilities
import pandas as pd


class Variables(enum.Enum):
    GOLDPRICE = 1
    GOOGLETRENDS = 2
    BLOCKREWARD = 3
    SNP500 = 4

#config
DONT_FETCH = []
FETCH = [Variables.BLOCKREWARD]
FETCH_FROM_JSON = []

GOLDPRICE_OUTPUT_FILE = "/goldprice.json"
GOOGLETRENDS_OUTPUT_FILE = "/googletrends.json"
BLOCKREWARD_OUTPUT_FILE = "/blockreward.json"
SNP500_OUTPUT_FILE = "/SnP500.json"

Run_Mode = Constants.Run_Mode
RUN_MODE = Constants.RUN_MODE

gold_df = pd.DataFrame()
google_trends_df = pd.DataFrame()
blockreward_df = pd.DataFrame()
s_n_p500_df = pd.DataFrame()

if Run_Mode.ONE_VARIABLE in RUN_MODE:
    if Variables.GOLDPRICE in FETCH:
        goldpricedata = api.CommodityPriceData("gold", Constants.start_date, Constants.end_date)
        gold_df = goldpricedata.fetchData()
        utilities.JsonConverter.exportDataFrameToJson(gold_df, Constants.JSON_OUTPUT_FOLDER, GOLDPRICE_OUTPUT_FILE)
        if Run_Mode.SHOW_DESCRIPTIVE in RUN_MODE:
            pass
    elif Variables.GOLDPRICE in FETCH_FROM_JSON:
        gold_df = utilities.JsonConverter.jsonToDataFrame(Constants.JSON_OUTPUT_FOLDER, GOLDPRICE_OUTPUT_FILE)
        if Run_Mode.SHOW_DESCRIPTIVE in RUN_MODE:
            pass
    elif Variables.BLOCKREWARD in FETCH:
        blockrewarddata = api.BlockRewardData(Constants.CHAIN_API_URL, "/block/", Constants.HEADERS_CHAIN_API)
        blockreward_df = blockrewarddata.fetchData()
        utilities.JsonConverter.exportDataFrameToJson(blockreward_df, Constants.JSON_OUTPUT_FOLDER, BLOCKREWARD_OUTPUT_FILE)
    elif Variables.BLOCKREWARD in FETCH_FROM_JSON:
        blockreward_df = utilities.JsonConverter.jsonToDataFrame(Constants.JSON_OUTPUT_FOLDER, BLOCKREWARD_OUTPUT_FILE)
        if Run_Mode.SHOW_DESCRIPTIVE in RUN_MODE:
            pass
    elif Variables.SNP500 in FETCH_FROM_JSON:
        sandp500data = api.SnP500Data(Constants.start_date, Constants.end_date)
        s_n_p500_df = sandp500data.fetchData()
        utilities.JsonConverter.exportDataFrameToJson(s_n_p500_df, Constants.JSON_OUTPUT_FOLDER, SNP500_OUTPUT_FILE)
    elif Variables.SNP500 in FETCH_FROM_JSON:
        s_n_p500_df = utilities.JsonConverter.jsonToDataFrame(Constants.JSON_OUTPUT_FOLDER, SNP500_OUTPUT_FILE)
        if Run_Mode.SHOW_DESCRIPTIVE in RUN_MODE:
            pass
    else:
        pass


elif Run_Mode.RUN_REGRESSION in RUN_MODE:
    pass


#concatenate data frames and remove non numerical columns(date)
data = pd.concat([gold_df, google_trends_df, blockreward_df, s_n_p500_df], axis=1, sort=False).select_dtypes(['number'])
#TODO merge on date
