class IdentifyPairs:
    def __init__(self, tradeable_pairs:list, individual_currencies:list = None, paired_order:list = None):
        self.tradeable_pairs = tradeable_pairs
        self.individual_currencies = individual_currencies
        self.paired_order = paired_order

        # Final Pairs
        self.tradeable_trio = self.paired_order if self._check_paired_order() else self.create_tradeable_trio()

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
        * False: If not present
        """
        # O(3*n) ~ O(n)
        if (self.paired_order):
            if (len(self.paired_order) == 3):
                for pair in self.paired_order:
                    IdentifyPairs._validate_paired_currency(pair)
                    if pair not in self.tradeable_pairs:
                        raise ValueError(f"{pair} not in tradeable_pairs list.")
            else:
                raise ValueError("paired_order can only have 3 elements.")
            print("All paired orders are present in the tradeable list.")
            return True
        return False

    def create_tradeable_trio(self):
        """
        Possible Approach:
        Empty list sol
        Create C(3, 2) pairs
        Till len(sol) < 3
        Iterate through tradeable list. 
        If item in tradeable list matches a pair in C(3, 2), append to sol.
        """
        pass
    
