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
    print("Obj1: ")
    obj1 = IdentifyPairs(coin_list, paired_order=["USDT_BTC", "USDT_ETH", "BTC_ETH"])
    print(obj1.get_tradeable_trio)
    print(obj1.get_all_tradeable_trios)

    print("\nObj2: ")
    obj2 = IdentifyPairs(coin_list, individual_currencies=["BTC", "ETH", "USDT"])
    print(obj2.get_tradeable_trio)
    print(obj2.get_all_tradeable_trios)

    print("\nObj3: ")
    obj3 = IdentifyPairs(coin_list)
    print(obj3.get_tradeable_trio)
    print(obj3.get_all_tradeable_trios)
    

