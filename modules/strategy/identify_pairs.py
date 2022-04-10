from itertools import permutations
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor

from modules.data.platform.btcmarkets import BTCMarkets
from modules.data.platform.independent_reserve import IndependentReserve
from modules.data.platform.oanda import Oanda
import pandas as pd


class IdentifyPairs:
    def __init__(self, currency_list: list = None, exchange_list: list = None,
                 paired_order: dict = None,
                 find_all: bool = False):

        # Option 1
        self.currency_list = currency_list
        self.exchange_list = exchange_list

        # Option 2
        self.paired_order = paired_order

        # Choice
        self.find_all = find_all

        # If paired order is given, check if it is valid
        self._trio_details = self._validate_paired_order()

    @property
    def get_tradeable_trio(self):
        return self._trio_details

    @property
    def get_all_tradeable_trios(self):
        return self._tradeable_all_pairs

    def _validate_paired_order(self):
        with ThreadPoolExecutor(max_workers=10) as pool:
            resp = list(pool.map(lambda args: args[1].get_details_for_pair(args[0]), list(self.paired_order.items())))

        return pd.concat(resp, ignore_index=True)

    @staticmethod
    def _validate_paired_currency(item: str):
        """
        Validate a currency pair by checking if "_" is present and two currencies on each side are present.
        """
        if ("_" not in item) or (len(item.split("_")) != 2):
            raise ValueError(
                f"{item}: Invalid Pair. Pair should be of the form <Currency>_<Currency>."
            )


if __name__ == "__main__":
    cur_dict1 = {
        "AUD_SGD": Oanda,
        "BTC_AUD": BTCMarkets,
        "XBT_SGD": IndependentReserve
    }

    # Initialise the object
    obj = IdentifyPairs(paired_order=cur_dict1)

    # Get trio details
    trio_details = obj.get_tradeable_trio

    print(trio_details)
