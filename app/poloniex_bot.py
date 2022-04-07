import sys
from pprint import pprint
import json

sys.path.append("..")
from modules.data.poloniex.poloniex_api import Poloniex as pl
from modules.strategy.identify_pairs import IdentifyPairs
from modules.strategy.conversion import Conversion
from modules.strategy.surface_arb import SurfaceArb

coin_price_url = "https://poloniex.com/public?command=returnTicker"


if __name__ == "__main__":
    data_obj = pl(coin_price_url)

    coin_list = data_obj.get_coins_tradeable

    ## Pairs
    # trio = IdentifyPairs(
    #     coin_list, paired_order=["USDT_BTC", "USDT_ETH", "BTC_ETH"]
    # ).get_tradeable_trio

    ## Trio details
    # trio_details = data_obj.get_details_for_trio(trio)
    # trio_prices = data_obj.get_price_for_trio(trio)

    # print(trio_prices)

    ## Main
    # ustd_btc_last = float(data_obj.json_resp["USDT_BTC"]["last"])
    # usdt_eth_last = float(data_obj.json_resp["USDT_ETH"]["last"])
    # btc_eth_last = float(data_obj.json_resp["BTC_ETH"]["last"])

    # multiplication_ = ustd_btc_last * btc_eth_last
    # print(multiplication_, usdt_eth_last, multiplication_ - usdt_eth_last)

    # obj1 = SurfaceArb(trio, trio_prices, 10000, "USDT")
    # pprint(obj1.get_trade_logs)
    # print()

    # obj2 = SurfaceArb(trio, trio_prices, 10, "BTC")
    # pprint(obj2.get_trade_logs)
    # print()

    # obj3 = SurfaceArb(trio, trio_prices, 50, "ETH")
    # pprint(obj3.get_trade_logs)
    # print()

    # Get Structured Pairs
    with open("structured_triangular_pairs.json") as json_file:
        structured_pairs = json.load(json_file)

    trio_list = []
    for t_pair in structured_pairs:
        trio_list.append(t_pair["combined"].split(","))

    for t in trio_list:
        obj1 = SurfaceArb(t, data_obj.get_price_for_trio(t), 1, t[0].split("_")[0])
        df = obj1.get_trade_logs
        if len(df[df["profit"] > 0]) > 0:
            print("-" * 100)
            print(obj1.trio)
            print(df)
            print("-" * 100)

# BTC   ETH
# USTD  BTC
#
# ETH/USDT
