from data_abstract import DataAbstract


class Data(DataAbstract):
    def __init__(self):
        super().__init__()

    def get_coins_tradeable(self):
        """
        List of possible tradeable pairs: <Currency>_<Currency>
        """
        pass

    def get_details_for_trio(self, trio: list):
        """
        Get the base and quote currencies
        """
        pass

    def get_price_for_trio(self, trio: list):
        """
        Pull prices for each pair from the respective APIs
        """
        pass

    def get_orderbook_for_trio(self, trio: list, depth: int):
        """
        Pull order book data for tro
        """
        pass
