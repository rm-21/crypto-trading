import sys
sys.path.append("..")
from modules.data.poloniex.poloniex_api import Poloniex as pl

coin_price_url = "https://poloniex.com/public?command=returnTicker"

class MainPoliniex(pl):
    def __init__(self, URL: str):
        super().__init__(URL)

if __name__ == "__main__":
    obj = MainPoliniex(coin_price_url)
    print(f"Number of Tradeable Coins: {len(obj.coins_tradeable)}")