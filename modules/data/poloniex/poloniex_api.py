from imp import is_frozen
import requests
import json
import time

class Poloniex:
    def __init__(self, URL: str):
        self._URL = URL

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

    @property
    def coin_list(self):
        self._get_coin_tickers()
        return self._collect_tradeables()
         
    