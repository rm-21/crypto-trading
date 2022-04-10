from modules.data.platform.btcmarkets import BTCMarkets
from modules.data.platform.independent_reserve import IndependentReserve
from modules.data.platform.oanda import Oanda
from modules.data.data_api import Data
from modules.strategy.identify_pairs import IdentifyPairs
from modules.strategy.surface_arb import SurfaceArb

"""
<Base>_<Quote>
1 Base = 'x' Quote
"""

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

    ## Check for Surface Arbitrage
    obj3 = SurfaceArb(trio_details, trio_prices, 100000, "AUD")
    trades_AUD = obj3.get_trade_logs

    obj4 = SurfaceArb(trio_details, trio_prices, 100000, "SGD")
    trades_SGD = obj4.get_trade_logs

    obj5 = SurfaceArb(trio_details, trio_prices, 1, "BTC")
    trades_BTC = obj5.get_trade_logs

    ## Print statements
    print(trades_AUD)
    print()
    print(trades_SGD)
    print()
    print(trades_BTC)
