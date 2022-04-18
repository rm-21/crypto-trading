import pandas as pd
import matplotlib.pyplot as plt
plt.style.use("seaborn-darkgrid")


class print_format:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

    @staticmethod
    def print_line(num_lines=100):
        print(print_format.BOLD + print_format.GREEN + "-" * num_lines + print_format.END)


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