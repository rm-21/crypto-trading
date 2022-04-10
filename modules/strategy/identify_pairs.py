from itertools import permutations
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
import pandas as pd


class IdentifyPairs:
    def __init__(self, paired_order: dict = None,
                 currency_list: list = None, exchange_list: list = None,
                 find_all: bool = False):

        # Option 1
        self.paired_order = paired_order

        # Option 2
        self.currency_list = currency_list
        self.exchange_list = exchange_list

        # Choice
        self.find_all = find_all

        # If paired order is given, check if it is valid
        self._trio_details = None
        self._get_trio_details()

    @property
    def get_tradeable_trio(self):
        return self._trio_details

    @property
    def get_all_tradeable_trios(self):
        pass

    def _get_trio_details(self):
        if self.paired_order:
            self._trio_details = self._validate_paired_order()
        else:
            self._trio_details = self._get_paired_order()

    def _validate_paired_order(self):
        with ThreadPoolExecutor(max_workers=10) as pool:
            resp = list(pool.map(lambda args: args[1].get_details_for_pair(args[0]), list(self.paired_order.items())))

        details = pd.concat(resp, ignore_index=True)

        check_series = pd.concat([details["baseAssetName"].value_counts(),
                                  details["quoteAssetName"].value_counts()], axis=1).sum(axis=1)
        if len(check_series[check_series != 2]) > 0:
            raise ValueError("Currency pairs are not correct. Please check that there is 2 of each currency.")
        return details

    def _get_paired_order(self):
        """
        To be implemented
        """
        pass


if __name__ == "__main__":
    from modules.data.platform.btcmarkets import BTCMarkets
    from modules.data.platform.independent_reserve import IndependentReserve
    from modules.data.platform.oanda import Oanda

    # cur_dict1 = {
    #     "AUD_SGD": Oanda,
    #     "BTC_AUD": BTCMarkets,
    #     "BTC_SGD": IndependentReserve
    # }
    cur_dict1 = {
        "AUD_SGD": Oanda,
        "BTC_AUD": BTCMarkets,
        "BTC_SGD": IndependentReserve
    }
    ## When paired object is given
    obj1 = IdentifyPairs(paired_order=cur_dict1)
    trio_details = obj1.get_tradeable_trio
    print(trio_details)

    ## When paired object is not given
    # list_cur = ["AUD", "SGD", "BTC"]
    # print(list(permutations(list_cur, 2)))
    # list_exch = [Oanda, IndependentReserve, BTCMarkets]
