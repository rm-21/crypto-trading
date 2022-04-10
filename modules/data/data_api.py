import sys

sys.path.append("..")
from data_abstract import DataAbstract
from modules.data.platform.btcmarkets import BTCMarkets
from modules.data.platform.independent_reserve import IndependentReserve
from modules.data.platform.oanda import Oanda


class Data(DataAbstract):
    def __init__(self, coin_1, coin_1_ex, coin_2, coin_2_ex, currency_pair, currency_ex):
        super().__init__()
        self.coin_1 = coin_1
        self.coin_1_ex = coin_1_ex

        self.coin_2 = coin_2
        self.coin_2_ex = coin_2_ex

        self.currency = currency_pair
        self.currency_ex = currency_ex

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
