from itertools import permutations
import json


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

    def _create_all_pairs(self, dump=True):
        """
        To be implemented
        """
        if (
            (self.paired_order == None or self.paired_order == False)
            and (self.individual_currencies == None)
        ) or (self.find_all):
            # Declare Variables
            triangular_pairs_list = []
            remove_duplicates_list = []
            pairs_list = self.tradeable_pairs[0:]

            # Get Pair A
            for pair_a in pairs_list:
                pair_a_split = pair_a.split("_")
                a_base = pair_a_split[0]
                a_quote = pair_a_split[1]

                # Assign A to a Box
                a_pair_box = [a_base, a_quote]

                # Get Pair B
                for pair_b in pairs_list:
                    pair_b_split = pair_b.split("_")
                    b_base = pair_b_split[0]
                    b_quote = pair_b_split[1]

                    # Check Pair B
                    if pair_b != pair_a:
                        if b_base in a_pair_box or b_quote in a_pair_box:

                            # Get Pair C
                            for pair_c in pairs_list:
                                pair_c_split = pair_c.split("_")
                                c_base = pair_c_split[0]
                                c_quote = pair_c_split[1]

                                # Count the number of matching C items
                                if pair_c != pair_a and pair_c != pair_b:
                                    combine_all = [pair_a, pair_b, pair_c]
                                    pair_box = [
                                        a_base,
                                        a_quote,
                                        b_base,
                                        b_quote,
                                        c_base,
                                        c_quote,
                                    ]

                                    counts_c_base = 0
                                    for i in pair_box:
                                        if i == c_base:
                                            counts_c_base += 1

                                    counts_c_quote = 0
                                    for i in pair_box:
                                        if i == c_quote:
                                            counts_c_quote += 1

                                    # Determining Triangular Match
                                    if (
                                        counts_c_base == 2
                                        and counts_c_quote == 2
                                        and c_base != c_quote
                                    ):
                                        combined = pair_a + "," + pair_b + "," + pair_c
                                        unique_item = "".join(sorted(combine_all))

                                        if unique_item not in remove_duplicates_list:
                                            match_dict = {
                                                "a_base": a_base,
                                                "b_base": b_base,
                                                "c_base": c_base,
                                                "a_quote": a_quote,
                                                "b_quote": b_quote,
                                                "c_quote": c_quote,
                                                "pair_a": pair_a,
                                                "pair_b": pair_b,
                                                "pair_c": pair_c,
                                                "combined": combined,
                                            }
                                            triangular_pairs_list.append(match_dict)
                                            remove_duplicates_list.append(unique_item)

            with open("structured_triangular_pairs.json", "w") as fp:
                json.dump(triangular_pairs_list, fp)

            return triangular_pairs_list
