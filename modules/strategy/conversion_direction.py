import networkx as nx
import pandas as pd


class Graph:
    def __init__(self, trio_details: pd.DataFrame, init_currency: str):
        self.trio_details = trio_details
        self.trio = self.trio_details["marketId"].tolist()
        self.init_currency = init_currency

    def get_paths(self):
        return self._create_paths()

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

    ## Check for Surface Arbitrage
    obj3 = Graph(trio_details, "AUD")
    obj4 = Graph(trio_details, "BTC")
    obj5 = Graph(trio_details, "SGD")

    ## Print statements
    print(obj3.get_paths())
    print(obj4.get_paths())
    print(obj5.get_paths())
