from imp import is_frozen
import requests
import json
import time

class Poloniex:
    """
    Parameters:
    URL: Link for the API Request

    Methods:
    coin_list: Returns the list of tradeable coins after filtering for frozen coins.
    """
    def __init__(self, URL: str):
        self._URL = URL
        self._coins_tradeable = self._coin_list()

    @property
    def get_coins_tradeable(self):
        return self._coins_tradeable

    def get_details_for_trio(self, trio: list):
        pair_1 = trio[0].split("_")
        pair_2 = trio[1].split("_")
        pair_3 = trio[2].split("_")

        return {
            "pair_1_base":pair_1[0],
            "pair_1_quote":pair_1[1],
            "pair_2_base": pair_2[0],
            "pair_2_quote": pair_2[1],
            "pair_3_base" : pair_3[0],
            "pair_3_quote": pair_3[1]
        }

    def get_price_for_trio(self, trio: list):
        # Individual currency pairs
        pair_1 = trio[0]
        pair_2 = trio[1]
        pair_3 = trio[2]

        return {
        "pair_1_ask": float(self.json_resp[pair_1]["lowestAsk"]),
        "pair_1_bid": float(self.json_resp[pair_1]["highestBid"]),
        "pair_2_ask": float(self.json_resp[pair_2]["lowestAsk"]),
        "pair_2_bid": float(self.json_resp[pair_2]["highestBid"]),
        "pair_3_ask": float(self.json_resp[pair_3]["lowestAsk"]),
        "pair_3_bid": float(self.json_resp[pair_3]["highestBid"])
        }


    def _get_coin_tickers(self):
        req = requests.get(self._URL)
        self.json_resp = json.loads(req.text)
        return self.json_resp

    def _collect_tradeables(self):
        coin_list = []
        for coin in self.json_resp:
            is_frozen = self.json_resp[coin]["isFrozen"]
            is_post_only = self.json_resp[coin]["postOnly"]
            if is_frozen == "0" and is_post_only == "0":
                coin_list.append(coin)
        return coin_list

    def _coin_list(self):
        self._get_coin_tickers()
        return self._collect_tradeables()
         
    