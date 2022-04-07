import sys
from pprint import pprint

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
    trio = IdentifyPairs(
        coin_list, paired_order=["USDT_BTC", "USDT_ETH", "BTC_ETH"]
    ).get_tradeable_trio

    ## Trio details
    trio_details = data_obj.get_details_for_trio(trio)
    trio_prices = data_obj.get_price_for_trio(trio)

    # print(trio_prices)

    ## Main
    obj1 = SurfaceArb(trio, trio_prices, 100, "USDT")
    pprint(obj1.get_trade_logs)
    print()

    obj2 = SurfaceArb(trio, trio_prices, 1, "BTC")
    pprint(obj2.get_trade_logs)
    print()

    obj3 = SurfaceArb(trio, trio_prices, 50, "ETH")
    pprint(obj3.get_trade_logs)
    print()
