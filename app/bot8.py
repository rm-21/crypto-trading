import datetime
import time
import os
from modules.data.platform.btcmarkets import BTCMarkets
from modules.data.platform.independent_reserve import IndependentReserve
from modules.data.platform.oanda import Oanda
from modules.data.data_api import Data
from modules.strategy.identify_pairs import IdentifyPairs
from modules.strategy.arbitrage import Arbitrage

"""
<Base>_<Quote>
1 Base = 'x' Quote
"""

def save_price_trade(timestamp, prices, trade_logs, path="..\\storage\\trade"):
    dir_ = path + f"\\{timestamp}"
    if not os.path.exists(dir_):
        os.makedirs(dir_)

    prices.to_csv(f"{path}\\{timestamp}\\prices.csv")
    trade_logs.to_csv(f"{path}\\{timestamp}\\trade_logs.csv")

def run_surface_arb(currency_dict: dict, init_amount=60000, init_cur="AUD", run_interval=1, max_duration=30,
                    path="..\\storage\\trade"):
    ## Trio details
    obj1 = IdentifyPairs(paired_order=currency_dict)
    trio_details = obj1.get_tradeable_trio

    obj2 = Data(trio_details)

    i = 0
    while i < max_duration:
        timestamp = datetime.datetime.now()
        print(f"{i + 1}: {timestamp}")
        ## Get data for TRIO based on details
        trio_prices = obj2.get_price_for_trio()

        ## Check for Surface Arbitrage
        obj3 = Arbitrage(trio_details, trio_prices, init_amount, init_cur)
        trades_log = obj3.get_trade_logs()

        ## Save
        save_price_trade(timestamp.timestamp(), trio_prices, trades_log, path=path)

        ## Print statements
        # print(trio_prices)
        print()
        if (trades_log["profit"] > 0).any():
            print("TRADE LOGS")
            print(trades_log.iloc[:, :5])
            print()
        i += 1
        time.sleep(run_interval)


if __name__ == "__main__":
    # cur_dict1 = {
    #     "AUD_SGD": Oanda,
    #     "BTC_AUD": BTCMarkets,
    #     "BTC_SGD": IndependentReserve
    # }
    #
    # run_surface_arb(cur_dict1, init_amount=60000, init_cur="AUD", run_interval=1, max_duration=3600,
    #                 path="..\\storage\\trade\\AUD_SGD_BTC")

    # cur_dict2 = {
    #     "AUD_USD": Oanda,
    #     "BTC_AUD": BTCMarkets,
    #     "BTC_USD": IndependentReserve
    # }
    #
    # run_surface_arb(cur_dict2, init_amount=50000, init_cur="USD", run_interval=1, max_duration=3600,
    #                 path="..\\storage\\trade\\AUD_USD_BTC")

    cur_dict3 = {
        "AUD_SGD": Oanda,
        "XLM_AUD": BTCMarkets,
        "XLM_SGD": IndependentReserve
    }

    run_surface_arb(cur_dict3, init_amount=60000, init_cur="AUD", run_interval=1, max_duration=30000,
                    path="..\\storage\\trade\\AUD_SGD_XLM")
    # print(BTCMarkets.get_coins_tradeable())
