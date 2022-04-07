import sys
from pprint import pprint

sys.path.append("..")
from modules.data.poloniex.poloniex_api import Poloniex as pl
from modules.strategy.identify_pairs import IdentifyPairs
from modules.strategy.conversion import Conversion
from modules.strategy.surface_arb import SurfaceArb

coin_price_url = "https://poloniex.com/public?command=returnTicker"


class MainPoliniex(pl):
    def __init__(self, URL: str):
        super().__init__(URL)


if __name__ == "__main__":
    ## Coin list
    main_obj = MainPoliniex(coin_price_url)
    coin_list = main_obj.get_coins_tradeable

    ## Pairs
    trio = IdentifyPairs(
        coin_list, paired_order=["USDT_BTC", "USDT_ETH", "BTC_ETH"]
    ).get_tradeable_trio

    ## Trio details
    trio_details = main_obj.get_details_for_trio(trio)
    trio_prices = main_obj.get_price_for_trio(trio)
    # print(trio_details)
    print(trio_prices)

    graph_obj = SurfaceArb(trio=trio, trio_prices=trio_prices)
    quotes = graph_obj._get_quote_to_use("USDT")
    # print(quotes)
    ## Conversion check
    # btc_to_usd = Conversion.currency_conversion(
    #     100,
    #     trio_details["pair_1_base"],
    #     trio_details["pair_1_quote"],
    #     trio_prices["pair_1_bid"],
    #     trio_prices["pair_1_ask"],
    #     "forward",
    # )
    # print(btc_to_usd)

    # usd_to_btc = Conversion.currency_conversion(
    #     btc_to_usd["new_amount"],
    #     trio_details["pair_1_base"],
    #     trio_details["pair_1_quote"],
    #     trio_prices["pair_1_bid"],
    #     trio_prices["pair_1_ask"],
    #     "reverse",
    # )
    # print(usd_to_btc)
