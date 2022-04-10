import pandas as pd
from data_abstract import DataAbstract
from concurrent.futures import ThreadPoolExecutor


class Data(DataAbstract):
    def __init__(self, trio: pd.DataFrame):
        super().__init__()
        self._trio_details = trio

    def get_details_for_trio(self):
        """
        Get the base and quote currencies
        """
        return self._trio_details

    def get_price_for_trio(self):
        """
        Pull prices for each pair from the respective APIs
        """
        paired_order = self._get_paired_order_dict()
        with ThreadPoolExecutor(max_workers=10) as pool:
            resp = list(pool.map(lambda args: args[1].get_price_for_pair(args[0]), list(paired_order.items())))
        prices = pd.concat(resp, ignore_index=True).set_index(keys=["marketId"])
        return prices

    def get_orderbook_for_trio(self):
        """
        Pull order book data for tro
        """
        paired_order = self._get_paired_order_dict()
        with ThreadPoolExecutor(max_workers=10) as pool:
            resp = list(pool.map(lambda args: args[1].get_orderbook_for_pair(args[0]), list(paired_order.items())))
        return resp

    def _get_paired_order_dict(self):
        paired_dict = dict(zip(self._trio_details["marketId"], self._trio_details["exchange_obj"]))
        return paired_dict


if __name__ == "__main__":
    from modules.strategy.identify_pairs import IdentifyPairs
    from modules.data.platform.btcmarkets import BTCMarkets
    from modules.data.platform.independent_reserve import IndependentReserve
    from modules.data.platform.oanda import Oanda

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
    # print(obj2.get_price_for_trio())
    for x in obj2.get_orderbook_for_trio():
        print(x[["market_id", "timestamp"]])
    # print(obj2.get_details_for_trio())
