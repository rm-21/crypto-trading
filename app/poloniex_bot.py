import sys
import time
from pprint import pprint

sys.path.append("..")
from modules.data.poloniex.poloniex_api import Poloniex as pl
from modules.strategy.deprecated.identify_pairs import IdentifyPairs
from modules.strategy.surface_arb import SurfaceArb

coin_price_url = "https://poloniex.com/public?command=returnTicker"


if __name__ == "__main__":
    data_obj = pl(coin_price_url)
    coin_list = data_obj.get_coins_tradeable

    ## Pairs
    trio = IdentifyPairs(
        coin_list, paired_order=["USDT_BTC", "USDT_ETH", "BTC_ETH"]
    ).get_tradeable_trio

    ## Depth
    # print("\nFormatted: FORWARD")
    # print(data_obj.get_depth_for_pair(trio[0])[0]["bids"])
    # print()
    # print(data_obj.get_depth_for_pair(trio[0])[0]["asks"])
    # print()
    # print("Formatted: REVERSE")
    # print(data_obj.get_depth_for_pair(trio[0])[1]["bids"])
    # print()
    # print(data_obj.get_depth_for_pair(trio[0])[1]["asks"])
    # print()

    # print(trio_prices)

    ## Main
    # ustd_btc_last = float(data_obj.json_resp["USDT_BTC"]["last"])
    # usdt_eth_last = float(data_obj.json_resp["USDT_ETH"]["last"])
    # btc_eth_last = float(data_obj.json_resp["BTC_ETH"]["last"])

    # multiplication_ = ustd_btc_last * btc_eth_last
    # print(multiplication_, usdt_eth_last, multiplication_ - usdt_eth_last)

    while True:
        ## Trio details
        trio_details = data_obj.get_details_for_trio(trio)
        trio_prices = data_obj.get_price_for_trio(trio)
        obj1 = SurfaceArb(trio, trio_prices, 10000, "USDT")
        pprint(obj1.get_trade_logs)
        time.sleep(1)
        print()

    # obj2 = SurfaceArb(trio, trio_prices, 10, "BTC")
    # pprint(obj2.get_trade_logs)
    # print()

    # obj3 = SurfaceArb(trio, trio_prices, 50, "ETH")
    # pprint(obj3.get_trade_logs)
    # print()

    # Get Structured Pairs
    # def tempFunc():
    #     all_pairs = IdentifyPairs(coin_list).get_all_tradeable_trios
    #     for t in all_pairs:
    #         obj2 = SurfaceArb(t, data_obj.get_price_for_trio(t), 1, t[0].split("_")[0])
    #         df = obj2.get_trade_logs
    #         if len(df[df["profit"] > 0].index) > 0:
    #             print("-" * 100)
    #             print(obj2.trio)
    #             print(df)
    #             print("-" * 100)

    # tempFunc()
