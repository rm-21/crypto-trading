import datetime
import time

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


def run_surface_arb(currency_dict: dict, init_amount=60000, init_cur="AUD", run_interval=1, max_duration=30):
    ## Trio details
    obj1 = IdentifyPairs(paired_order=currency_dict)
    trio_details = obj1.get_tradeable_trio

    i = 0
    while i < max_duration:
        print(f"{i + 1}: {datetime.datetime.now()}")
        ## Get data for TRIO based on details
        obj2 = Data(trio_details)
        trio_prices = obj2.get_price_for_trio()

        ## Check for Surface Arbitrage
        obj3 = SurfaceArb(trio_details, trio_prices, init_amount, init_cur)
        trades_log = obj3.get_trade_logs

        ## Print statements
        # print(trio_prices)
        print()
        if (trades_log["profit"] > 0).any():
            print(trades_log.iloc[:, :5])
            print()
        i += 1
        time.sleep(run_interval)


if __name__ == "__main__":
    cur_dict1 = {
        "AUD_SGD": Oanda,
        "BTC_AUD": BTCMarkets,
        "BTC_SGD": IndependentReserve
    }

    run_surface_arb(cur_dict1, init_amount=60000, init_cur="AUD", run_interval=1, max_duration=3600)
