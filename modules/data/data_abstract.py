from abc import ABC, abstractmethod


class DataAbstract(ABC):
    @abstractmethod
    def get_details_for_trio(self):
        """
        Get the base and quote currencies
        """
        pass

    @abstractmethod
    def get_price_for_trio(self):
        """
        Pull prices for each pair from the respective APIs
        """
        pass

    @abstractmethod
    def get_orderbook_for_trio(self):
        """
        Pull order book data for tro
        """
        pass
