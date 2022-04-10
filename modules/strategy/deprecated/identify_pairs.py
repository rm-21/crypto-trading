from itertools import permutations
from collections import defaultdict


class IdentifyPairs:
    def __init__(
        self,
        tradeable_pairs: list,
        individual_currencies: list = None,
        paired_order: list = None,
        find_all: bool = False,
    ):
        self.tradeable_pairs = tradeable_pairs
        self.individual_currencies = individual_currencies
        self.paired_order = paired_order
        self.find_all = find_all

        ## Final Pairs
        # 1. If paired_order is there, validate it and see if it is present in the tradeable_pairs list
        # 2. If 1 is false, and individual currencies are present, create trio and check as in 1
        self._tradeable_trio = (
            self.paired_order
            if self._check_paired_order()
            else self._create_tradeable_trio_from_individual()
        )

        ## Complete List of tradeable pairs
        # If Final Pairs is None OR find_all == True
        # Create all trios based on tradeable_pairs list.
        self._tradeable_all_pairs = self._create_all_pairs()

    @property
    def get_tradeable_trio(self):
        return self._tradeable_trio

    @property
    def get_all_tradeable_trios(self):
        return self._tradeable_all_pairs

    @staticmethod
    def _validate_paired_currency(item: str):
        """
        Validate a currency pair by checking if "_" is present and two currencies on each side are present.
        """
        if ("_" not in item) or (len(item.split("_")) != 2):
            raise ValueError(
                f"{item}: Invalid Pair. Pair should be of the form <Currency>_<Currency>."
            )

    def _check_paired_order(self):
        """
        Checks whether the paired_order is present in the tradeable_pairs list.

        Returns:
        * True: If present
        """
        # O(3*n) ~ O(n)
        if self.paired_order:
            if len(self.paired_order) == 3:
                for pair in self.paired_order:
                    IdentifyPairs._validate_paired_currency(pair)
                    if pair not in self.tradeable_pairs:
                        raise ValueError(f"{pair} not in tradeable_pairs list.")
            else:
                raise ValueError("Paired_order can only have 3 elements.")
            print("All paired orders are present in the tradeable list.")
            return True

    def _create_tradeable_trio_from_individual(self):
        """
        If paired_order:
        * is None

        Returns:
        * tradeable_trio: if individual_currencies is not None
        * False: otherwise
        """
        trio = []
        if (self.paired_order == None) and (self.individual_currencies):
            all_possible_pairs = list(permutations(self.individual_currencies, 2))
            self.paired_order = list(map(lambda x: "_".join(x), all_possible_pairs))

            while len(trio) < 3:
                for pair in self.paired_order:
                    IdentifyPairs._validate_paired_currency(pair)
                    if pair in self.tradeable_pairs:
                        trio.append(pair)
                return trio
        return False

    def _create_all_pairs(self):
        tri_pair_list = []
        pair_dict = defaultdict(list)
        for pair in self.tradeable_pairs:
            base, quote = pair.split("_")[0], pair.split("_")[1]
            pair_dict[base].append(quote)

        for k, v in pair_dict.items():
            for idx1 in range(len(v)):
                pair_1 = k + "_" + v[idx1]

                for idx2 in range(idx1 + 1, len(v)):
                    temp_pair = []

                    temp_pair.append(pair_1)

                    pair_2 = k + "_" + v[idx2]
                    temp_pair.append(pair_2)

                    pair_3_itr1 = v[idx1] + "_" + v[idx2]
                    pair_3_itr2 = v[idx2] + "_" + v[idx1]

                    if pair_3_itr1 in self.tradeable_pairs:
                        temp_pair.append(pair_3_itr1)
                    elif pair_3_itr2 in self.tradeable_pairs:
                        temp_pair.append(pair_3_itr2)

                    if len(temp_pair) == 3:
                        tri_pair_list.append(temp_pair)

        return tri_pair_list


if __name__ == "__main__":
    ## Boiler
    import sys

    sys.path.append("../..")
    from modules.data.poloniex.poloniex_api import Poloniex as pl
    from modules.strategy.deprecated.identify_pairs import IdentifyPairs

    coin_price_url = "https://poloniex.com/public?command=returnTicker"
    data_obj = pl(coin_price_url)

    coin_list = data_obj.get_coins_tradeable

    ## Main
    obj = IdentifyPairs(coin_list)
    print(obj._create_all_pairs())
