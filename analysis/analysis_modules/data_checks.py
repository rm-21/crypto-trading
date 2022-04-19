import pandas as pd
import matplotlib.pyplot as plt
from analysis.analysis_modules.print_format import print_format
plt.style.use("seaborn-darkgrid")


class BasicDataChecks:
    pd.set_option('expand_frame_repr', False)

    def __init__(self, data_loc):
        self._data = pd.read_pickle(data_loc)

    @property
    def data(self):
        return self._data

    def check_null(self):
        return self._data.isnull().sum()

    def check_duplicates(self):
        if self._data.duplicated().sum() > 0:
            return self._data[self._data.duplicated(keep=False)]
        return self._data.duplicated().sum()

    @property
    def check(self):
        print_format.print_line()
        print(print_format.BOLD + "Data head: " + print_format.END)
        print(self._data.head())
        print_format.print_line()
        print(print_format.BOLD + "Data tail:  " + print_format.END)
        print(self._data.tail())
        print_format.print_line()
        print(print_format.BOLD + "Null Values: " + print_format.END)
        print(self.check_null())
        print_format.print_line()
        print(print_format.BOLD + "Duplicate Values: " + print_format.END)
        print(self.check_duplicates())
        print_format.print_line()
        print(print_format.BOLD + "Data Info: " + print_format.END)
        print(self._data.info())
        print_format.print_line()
        print(print_format.BOLD + "Data Description: " + print_format.END)
        print(self._data.describe())
        print_format.print_line()
        return None
