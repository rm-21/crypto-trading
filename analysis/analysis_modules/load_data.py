import os
import pandas as pd
import datetime

class LoadData:
    def __init__(self, path: str, trio: str, pair1: str, pair2: str, pair3: str):
        self._path = path + "\\" + trio
        self._trio = trio
        self._pair1 = pair1
        self._pair2 = pair2
        self._pair3 = pair3

        self._timestamps = os.listdir(self._path)

        self._price_data = None

    @property
    def price_data(self):
        self._price_data = self._create_dataframe()
        return self._price_data

    def _create_index(self):
        index = [datetime.datetime.fromtimestamp(float(_)) for _ in self._timestamps]
        return index

    def _create_columns(self):
        tuples = [(self._pair1, "bestBid"), (self._pair1, "bestAsk"),
                  (self._pair2, "bestBid"), (self._pair2, "bestAsk"),
                  (self._pair3, "bestBid"), (self._pair3, "bestAsk"),
                  ("trade", "trade0"), ("trade", "trade1")]
        columns = pd.MultiIndex.from_tuples(tuples)
        return columns

    def _create_dataframe(self):
        columns = self._create_columns()
        index = self._create_index()
        dataframe = pd.DataFrame(columns=columns, index=index).sort_index()

        for ts in self._timestamps:
            price_path = f"{self._path}\\{ts}\\prices.csv"
            trades_path = f"{self._path}\\{ts}\\trade_logs.csv"

            try:
                prices_data = pd.read_csv(price_path, index_col=0, usecols=[0, 1, 2]).stack()
                dataframe.loc[datetime.datetime.fromtimestamp(float(ts))][:6] = prices_data

                trades_data = pd.read_csv(trades_path, index_col=0).loc[["0_trade3", "1_trade3"]]["percent"]
                dataframe.loc[datetime.datetime.fromtimestamp(float(ts))][6:] = trades_data
            except ValueError:
                dataframe.drop(datetime.datetime.fromtimestamp(float(ts)), inplace=True)
        return dataframe
