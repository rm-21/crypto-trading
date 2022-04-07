class IdentifyPairs:
    def __init__(self, tradeable_pairs:list, individual_currencies:list = None, paired_order:list = None):
        self.tradeable_pairs = tradeable_pairs
        self.individual_currencies = individual_currencies
        self.paired_order = paired_order
        
        # Final Pairs
        self.tradeable_trio = self.paired_order if self._check_paired_order() else self.create_tradeable_trio()

    @staticmethod
    def _validate_paired_currency(item: str):
        if "_" not in item:
            raise ValueError(f"{item}: Invalid Pair. Pair should be of the form <Currency>_<Currency>.")

    def _check_paired_order(self):
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
        pass
    
