from modules.data.platform.btcmarkets import BTCMarkets
from modules.data.platform.independent_reserve import IndependentReserve
from modules.data.platform.oanda import Oanda
from modules.data.data_api import Data
from modules.strategy.identify_pairs import IdentifyPairs
from modules.strategy.surface_arb import SurfaceArb

if __name__ == "__main__":
    cur_dict1 = {
        "AUD_SGD": Oanda,
        "BTC_AUD": BTCMarkets,
        "BTC_SGD": IndependentReserve
    }

    ## Trio details
    obj1 = IdentifyPairs(paired_order=cur_dict1)
    trio_details = obj1.get_tradeable_trio

    ## Get data for TRIO based on details
    obj2 = Data(trio_details)
    trio_prices = obj2.get_price_for_trio()
    print(trio_prices)

    ## Check for Surface Arbitrage

