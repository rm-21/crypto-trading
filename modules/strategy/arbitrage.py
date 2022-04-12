import pandas as pd
from modules.strategy.conversion import Conversion
from modules.strategy.conversion_direction import Graph


class Arbitrage:
    def __init__(self, trio_details: pd.DataFrame, trio_prices: pd.DataFrame, init_amount: float, init_currency: str):
        self.trio_details = trio_details
        self.trio_prices = trio_prices

        self.trio = self.trio_details["marketId"].tolist()

        self.init_amount = init_amount
        self.init_currency = init_currency
        self.TRADES_LOG = pd.DataFrame(columns=["new_amount", "denomination", "swap_rate", "direction", "profit", "percent"])
        
    def get_trade_logs(self):
        self._get_surface_arb()

        idx_temp = self.TRADES_LOG.index
        for i in range(2, len(idx_temp), 3):
            self.TRADES_LOG.loc[idx_temp[i], "profit"] = (
                    self.TRADES_LOG.loc[idx_temp[i], "new_amount"] - self.init_amount
            )

            self.TRADES_LOG.loc[idx_temp[i], "percent"] = (
                    self.TRADES_LOG.loc[idx_temp[i], "profit"] / self.init_amount
            )

        return self.TRADES_LOG

    def _get_surface_arb(self):
        quotes = self._get_quote_to_use()

        for idx, itr in enumerate(quotes):
            self._run_iteration(itr, idx)

    def _get_quote_to_use(self):
        quotes_to_use = []
        paths = Graph(self.trio_details, self.init_currency).get_paths()

        for path in paths:
            path_details = []
            for i in range(1, len(path)):
                quote_1 = path[i] + "_" + path[i - 1]
                quote_2 = path[i - 1] + "_" + path[i]

                if quote_1 in self.trio:
                    params = {
                        "base_currency": path[i],
                        "quote_currency": path[i - 1],
                        "bid": self.trio_prices.loc[quote_1]["bestBid"],
                        "ask": self.trio_prices.loc[quote_1]["bestAsk"],
                        "direction": "reverse",
                    }

                    path_details.append(params)

                elif quote_2 in self.trio:
                    params = {
                        "base_currency": path[i - 1],
                        "quote_currency": path[i],
                        "bid": self.trio_prices.loc[quote_2]["bestBid"],
                        "ask": self.trio_prices.loc[quote_2]["bestAsk"],
                        "direction": "forward",
                    }
                    path_details.append(params)

            quotes_to_use.append(path_details)
        return quotes_to_use

    def _run_iteration(self, iteration, idx):
        if len(iteration) != 3:
            raise ValueError("Issue with self._get_quote_to_use().")

        step1_params = iteration[0]
        step1_params["init_amount"] = self.init_amount
        step1 = Conversion.currency_conversion(**step1_params)
        self.TRADES_LOG.loc[f"{idx}_trade1"] = list(step1.values()) + [0, 0]

        step2_params = iteration[1]
        step2_params["init_amount"] = step1["new_amount"]
        step2 = Conversion.currency_conversion(**step2_params)
        self.TRADES_LOG.loc[f"{idx}_trade2"] = list(step2.values()) + [0, 0]

        step3_params = iteration[2]
        step3_params["init_amount"] = step2["new_amount"]
        step3 = Conversion.currency_conversion(**step3_params)
        self.TRADES_LOG.loc[f"{idx}_trade3"] = list(step3.values()) + [0, 0]

        if step3["denomination"] != self.init_currency:
            raise ValueError(
                "Surface arbitrage not implemented properly. Initial currency is not equal to the final currency"
            )


if __name__ == "__main__":
    from modules.data.platform.btcmarkets import BTCMarkets
    from modules.data.platform.independent_reserve import IndependentReserve
    from modules.data.platform.oanda import Oanda
    from modules.data.data_api import Data
    from modules.strategy.identify_pairs import IdentifyPairs
    from pprint import pprint

    cur_dict1 = {
        "AUD_SGD": Oanda,
        "BTC_AUD": BTCMarkets,
        "BTC_SGD": IndependentReserve
    }

    ## Trio details
    obj1 = IdentifyPairs(paired_order=cur_dict1)
    trio_details = obj1.get_tradeable_trio

    ## Get data for TRIO based on details
    obj2 = Data(trio_details)
    trio_prices = obj2.get_price_for_trio()

    ## Check for Surface Arbitrage
    obj3 = Arbitrage(trio_details, trio_prices, 100000, "AUD")

    ## Print statements
    # print(trio_prices)
    # print()
    # print(Graph(trio_details, "AUD").get_paths())
    # print()
    # pprint(obj3._get_quote_to_use())
    print(obj3.get_trade_logs())

    # print(BTCMarkets.get_coins_tradeable())
    # print(IndependentReserve.get_coins_tradeable())
