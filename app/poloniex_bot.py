import sys

from pip import main

sys.path.append("..")
from modules.data.poloniex.poloniex_api import Poloniex as pl
from modules.strategy.identify_pairs import IdentifyPairs
from modules.strategy.conversion import Conversion

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

    ## Conversion check
    btc_to_usd = Conversion.currency_conversion(
        100,
        trio_details["pair_1_base"],
        trio_details["pair_1_quote"],
        trio_prices["pair_1_bid"],
        trio_prices["pair_1_ask"],
        "forward",
    )
    print(btc_to_usd)

    usd_to_btc = Conversion.currency_conversion(
        btc_to_usd["new_amount"],
        trio_details["pair_1_base"],
        trio_details["pair_1_quote"],
        trio_prices["pair_1_bid"],
        trio_prices["pair_1_ask"],
        "reverse",
    )
    print(usd_to_btc)
