import networkx as nx
import pandas as pd
from modules.strategy.conversion import Conversion


class SurfaceArb:
    TRADES_LOG = pd.DataFrame(columns=["new_amount", "denomination", "swap_rate", "direction", "profit", "percent"])

    def __init__(self, trio_details: pd.DataFrame, trio_prices: pd.DataFrame, init_amount: float, init_currency: str):
        self.trio_details = trio_details
        self.trio_prices = trio_prices

        self.trio = self.trio_details["marketId"].tolist()

        self.init_amount = init_amount
        self.init_currency = init_currency

    def _create_edges(self):
        edges = []
        for pair in self.trio:
            currencies = pair.split("_")
            tuple_1 = (currencies[0], currencies[1])
            tuple_2 = (currencies[1], currencies[0])
            edges = edges + [tuple_1, tuple_2]

        return edges

    def _create_paths(self):
        G = nx.Graph()
        G.add_edges_from(self._create_edges())

        node_to_cycles = {}
        for source in G.nodes():
            paths = []
            for target in G.neighbors(source):
                paths += [
                    l + [source]
                    for l in list(nx.all_simple_paths(G, source=source, target=target))
                    if len(l) > 2
                ]
            node_to_cycles[source] = paths
        return node_to_cycles[self.init_currency]

    def _get_quote_to_use(self):
        quotes_to_use = []
        paths = self._create_paths()
        for path in paths:
            path_details = []
            for i in range(1, len(path)):
                quote_1 = path[i] + "_" + path[i - 1]
                quote_2 = path[i - 1] + "_" + path[i]

                if quote_1 in self.trio:
                    idx = self.trio.index(quote_1)
                    bid_key = f"pair_{idx + 1}_bid"
                    ask_key = f"pair_{idx + 1}_ask"

                    params = {
                        "base_currency": path[i],
                        "quote_currency": path[i - 1],
                        "bid": self.trio_prices[bid_key],
                        "ask": self.trio_prices[ask_key],
                        "direction": "reverse",
                    }

                    path_details.append(params)

                elif quote_2 in self.trio:
                    idx = self.trio.index(quote_2)
                    bid_key = f"pair_{idx + 1}_bid"
                    ask_key = f"pair_{idx + 1}_ask"

                    params = {
                        "base_currency": path[i - 1],
                        "quote_currency": path[i],
                        "bid": self.trio_prices[bid_key],
                        "ask": self.trio_prices[ask_key],
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
        SurfaceArb.TRADES_LOG.loc[f"{idx}_trade1"] = list(step1.values()) + [0, 0]

        step2_params = iteration[1]
        step2_params["init_amount"] = step1["new_amount"]
        step2 = Conversion.currency_conversion(**step2_params)
        SurfaceArb.TRADES_LOG.loc[f"{idx}_trade2"] = list(step2.values()) + [0, 0]

        step3_params = iteration[2]
        step3_params["init_amount"] = step2["new_amount"]
        step3 = Conversion.currency_conversion(**step3_params)
        SurfaceArb.TRADES_LOG.loc[f"{idx}_trade3"] = list(step3.values()) + [0, 0]

        if step3["denomination"] != self.init_currency:
            raise ValueError(
                "Surface arbitrage not implemented properly. Initial currency is not equal to the final currency"
            )

    def _get_surface_arb(self):
        quotes = self._get_quote_to_use()

        for idx, itr in enumerate(quotes):
            self._run_iteration(itr, idx)

    @property
    def get_trade_logs(self):
        self._get_surface_arb()

        idx_temp = SurfaceArb.TRADES_LOG.index
        for i in range(2, len(idx_temp), 3):
            SurfaceArb.TRADES_LOG.loc[idx_temp[i], "profit"] = (
                SurfaceArb.TRADES_LOG.loc[idx_temp[i], "new_amount"] - self.init_amount
            )

            SurfaceArb.TRADES_LOG.loc[idx_temp[i], "percent"] = (
                SurfaceArb.TRADES_LOG.loc[idx_temp[i], "profit"] / self.init_amount
            )

        return SurfaceArb.TRADES_LOG


if __name__ == "__main__":
    from modules.data.platform.btcmarkets import BTCMarkets
    from modules.data.platform.independent_reserve import IndependentReserve
    from modules.data.platform.oanda import Oanda
    from modules.data.data_api import Data
    from modules.strategy.identify_pairs import IdentifyPairs

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
    obj3 = SurfaceArb(trio_details, trio_prices, 10000, "AUD")

    ## Print statements
    # print(trio_details)
    print(obj3._create_paths())

    # ## Boiler
    # import sys
    # from pprint import pprint
    #
    # sys.path.append("..")
    # from modules.data.poloniex.poloniex_api import Poloniex as pl
    # from modules.strategy.deprecated.identify_pairs import IdentifyPairs
    #
    # coin_price_url = "https://poloniex.com/public?command=returnTicker"
    # data_obj = pl(coin_price_url)
    #
    # coin_list = data_obj.get_coins_tradeable
    #
    # ## Pairs
    # trio = IdentifyPairs(
    #     coin_list, paired_order=["USDT_BTC", "USDT_ETH", "BTC_ETH"]
    # ).get_tradeable_trio
    #
    # ## Trio details
    # trio_details = data_obj.get_details_for_trio(trio)
    # trio_prices = data_obj.get_price_for_trio(trio)
    #
    # # print(trio_prices)
    #
    # ## Main
    # obj1 = SurfaceArb(trio, trio_prices, 100, "USDT")
    # pprint(obj1.get_trade_logs)
    # print()
    #
    # obj2 = SurfaceArb(trio, trio_prices, 1, "BTC")
    # pprint(obj2.get_trade_logs)
    # print()
    #
    # obj3 = SurfaceArb(trio, trio_prices, 50, "ETH")
    # pprint(obj3.get_trade_logs)
    # print()
