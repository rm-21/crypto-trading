import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from analysis.analysis_modules.print_format import print_format
plt.style.use("seaborn-whitegrid")


class DataExploration:
    def __init__(self, data: pd.DataFrame, filter_above_secs = 60):
        self._data = data
        self._filter_above_secs = filter_above_secs

        self._calc_arb_duration_time_diff()

    @property
    def data(self):
        return self._data

    def count_arbitrage_opportunities(self, plot=True, ret=False):
        profit_percent = self._data["trade"][self._data["trade"] > 0].count() / self._data["trade"].count()

        if plot:
            print(print_format.BLUE + print_format.BOLD + "Percentage of Scanned Profitable Trades" + print_format.END)
            ax = profit_percent[["trade0", "trade1"]].plot(kind='bar', rot=45, figsize=(8, 5))
            ax.text(0.0, profit_percent["trade0"]+0.0025, f"{round(profit_percent.trade0 * 100, 2)}%")
            ax.text(0.95, profit_percent["trade1"]+0.0025, f"{round(profit_percent.trade1 * 100, 2)}%")

        if ret:
            return profit_percent

    def unique_arb_opportunities(self, plot=True, ret=False):
        unique_profit_percent = self._data["trade", "arb_duration"][(self._data["trade", "trade0"] > 0) | (self._data["trade", "trade1"] > 0)].count()/len(self._data)
        unique_profit_percent = pd.Series(unique_profit_percent)

        if plot:
            print(print_format.BLUE + print_format.BOLD + "Percentage of Unique Profitable Trades" + print_format.END)
            ax = unique_profit_percent.plot(kind='bar', rot=45, figsize=(6, 5))
            ax.text(0.0, unique_profit_percent+0.0025, f"{round(unique_profit_percent[0] * 100, 4)}%")
            ax.set_xticklabels(["Unique"])

        if ret:
            return unique_profit_percent

    def average_arb_duration(self, filter_seconds=60, plot=True, ret=True):
        avg_dur = self._data[self._data["trade", "time_diff"] <= filter_seconds]
        avg_dur = avg_dur[(avg_dur["trade", "trade0"] > 0) | (avg_dur["trade", "trade1"] > 0)]

        # Unique Trades
        arb_dur_mask = ~(avg_dur["trade", "arb_duration"].isnull())
        avg_dur = avg_dur[arb_dur_mask]

        if plot:
            sns.set(rc={'figure.figsize': (5, int(filter_seconds / 5))})
            print(print_format.BLUE + print_format.BOLD + "Duration Distribution of Profitable Arb. Opportunities" + print_format.END)
            ax = sns.violinplot(data=avg_dur["trade", "arb_duration"],
                                color=(np.random.random(), np.random.random(), np.random.random()),
                                inner='box', grid=True)
            ax.get_children()[1].set_color('k')
            ax.get_children()[1].set_lw(5)

            ax.get_children()[2].set_color('w')
            ax.get_children()[3].set_color('w')
            ax.set_xticks([])
            ax.set_yticks([_ for _ in range(0, filter_seconds + 1, 2)])
            ax.axhline(avg_dur["trade", "arb_duration"].mean(), color='red', lw=2)
            ax.legend({f'Mean {round(avg_dur["trade", "arb_duration"].mean(), 3)}': avg_dur["trade", "arb_duration"].mean()})

        if ret:
            return avg_dur

    def _filter_extremes(self, copy_frame):
        indices = copy_frame[copy_frame["time_diff"] > self._filter_above_secs].index
        copy_frame = copy_frame.drop(indices)
        return copy_frame

    def _calc_arb_duration_time_diff(self):
        copy_frame = self._data.copy(deep=True).sort_index()
        copy_frame_trade = copy_frame["trade"].copy(deep=True)

        trade_data = self._create_time_calculated_data(copy_frame_trade)
        copy_frame["trade", "time_diff"] = trade_data["time_diff"]
        copy_frame["trade", "arb_duration"] = trade_data["arb_duration"]

        # Update dataframe to remove filtered rows
        # copy_frame.dropna(subset=[("trade", "time_diff")], inplace=True)

        self._data = copy_frame

    def _create_time_calculated_data(self, copy_frame: pd.DataFrame,):
        # Calculate time_diff
        copy_frame_with_time_diff = DataExploration._calculate_time_diff(copy_frame)

        # Filter time_diff
        # copy_frame_with_time_diff = self._filter_extremes(copy_frame_with_time_diff)

        # Calculate arb duration
        copy_frame_with_arb_dur_and_time_diff = DataExploration._calculate_arb_duration(copy_frame_with_time_diff)

        return copy_frame_with_arb_dur_and_time_diff

    @staticmethod
    def _calculate_arb_duration(copy_frame: pd.DataFrame):
        # Legacy position & arb duration vars
        legacy_pos = 0
        copy_frame["arb_duration"] = np.nan

        # Calculate arb duration if repeated
        for bar in range(len(copy_frame)):
            if (copy_frame.iloc[bar] != copy_frame.iloc[legacy_pos]).all():
                # Calculate length for which arb stays
                duration = copy_frame.iloc[bar].name - copy_frame.iloc[legacy_pos].name

                # Append to copy_frame
                copy_frame.loc[copy_frame.iloc[bar].name, "arb_duration"] = duration.total_seconds()

                # Update legacy position
                legacy_pos = bar
        return copy_frame

    @staticmethod
    def _calculate_time_diff(copy_frame: pd.DataFrame):
        copy_frame["time_diff"] = copy_frame.index.to_series().diff().apply(lambda val: abs(val.total_seconds()))
        return copy_frame

