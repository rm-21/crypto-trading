from itertools import permutations

class IdentifyPairs:
    def __init__(self, tradeable_pairs:list, individual_currencies:list = None, paired_order:list = None, find_all:bool = False):
        self.tradeable_pairs = tradeable_pairs
        self.individual_currencies = individual_currencies
        self.paired_order = paired_order
        self.find_all = find_all

        ## Final Pairs
        # 1. If paired_order is there, validate it and see if it is present in the tradeable_pairs list
        # 2. If 1 is false, and individual currencies are present, create trio and check as in 1
        self.tradeable_trio = self.paired_order if self._check_paired_order() else self.create_tradeable_trio_from_individual()

        ## Complete List of tradeable pairs
        # If Final Pairs is None OR find_all == True
        # Create all trios based on tradeable_pairs list.
        self.tradeable_all_pairs = self._create_all_pairs()

    @staticmethod
    def _validate_paired_currency(item: str):
        """
        Validate a currency pair by checking if "_" is present and two currencies on each side are present.
        """
        if ("_" not in item) or (len(item.split("_")) != 2):
            raise ValueError(f"{item}: Invalid Pair. Pair should be of the form <Currency>_<Currency>.")

    def _check_paired_order(self):
        """
        Checks whether the paired_order is present in the tradeable_pairs list.
        
        Returns:
        * True: If present
        """
        # O(3*n) ~ O(n)
        if (self.paired_order):
            if (len(self.paired_order) == 3):
                for pair in self.paired_order:
                    IdentifyPairs._validate_paired_currency(pair)
                    if pair not in self.tradeable_pairs:
                        raise ValueError(f"{pair} not in tradeable_pairs list.")
            else:
                raise ValueError("Paired_order can only have 3 elements.")
            print("All paired orders are present in the tradeable list.")
            return True

    def create_tradeable_trio_from_individual(self):
        """
        If paired_order: 
        * is None
        
        Returns: 
        * tradeable_trio: if individual_currencies is not None
        * False: otherwise
        """
        trio = []
        if (self.paired_order == None) and (self.individual_currencies):
            all_possible_pairs =  list(permutations(self.individual_currencies, 2))
            self.paired_order = list(map(lambda x: "_".join(x), all_possible_pairs))

            while (len(trio) < 3):
                for pair in self.paired_order:
                    IdentifyPairs._validate_paired_currency(pair)
                    if pair in self.tradeable_pairs:
                        trio.append(pair)
                return trio
        return False

    def _create_all_pairs(self):
        if ((self.paired_order == None) and (self.individual_currencies == None)) or (self.find_all):
            pass
        return None
