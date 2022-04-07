import sys
sys.path.append("..")
from modules.data.poloniex.poloniex_api import Poloniex as pl
from modules.strategy.identify_pairs import IdentifyPairs

coin_price_url = "https://poloniex.com/public?command=returnTicker"

class MainPoliniex(pl):
    def __init__(self, URL: str):
        super().__init__(URL)

if __name__ == "__main__":
    ## Coin list
    coin_list = MainPoliniex(coin_price_url).coins_tradeable
    # print(coin_list)

    ## Pairs identification
    # obj = IdentifyPairs(coin_list, paired_order=["USDT_BTC", "USDT_ETH", "BTC_ETH"])
    # obj = IdentifyPairs(coin_list, individual_currencies=["BTC", "ETH", "USDT"])
    obj = IdentifyPairs(coin_list)
    print(obj.tradeable_trio)

