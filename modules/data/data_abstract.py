from abc import ABC, abstractmethod


class DataAbstract(ABC):
    @abstractmethod
    def get_coins_tradeable(self):
        """
        List of possible tradeable pairs: <Currency>_<Currency>
        """
        pass

    @abstractmethod
    def get_details_for_trio(self, trio: list):
        """
        Get the base and quote currencies
        """
        pass

    @abstractmethod
    def get_price_for_trio(self, trio: list):
        """
        Pull prices for each pair from the respective APIs
        """
        pass

    @abstractmethod
    def get_orderbook_for_trio(self, trio: list, depth: int):
        """
        Pull order book data for tro
        """
        pass
