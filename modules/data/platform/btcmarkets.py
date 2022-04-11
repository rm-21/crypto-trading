import pandas as pd
import requests
import json
pd.set_option('display.max_columns', 20)
from datetime import datetime


class BTCMarkets:
    BASE_URL = "https://api.btcmarkets.net/v3"

    def __init__(self, market_id: str):
        self.market_id = BTCMarkets._validate_currency_pair(market_id)
        self._check_currency_exists()

    @staticmethod
    def get_coins_tradeable():
        """
        List of possible tradeable pairs: <Currency>_<Currency>
        """
        coins_tradeable = BTCMarkets._coins_tradeable()
        return coins_tradeable

    def get_details_for_pair(self, as_dict: bool = False):
        """
        Get the base and quote currencies
        """
        pair_details = self._details_for_pair()
        if as_dict:
            return pair_details.to_dict(orient='list')
        return pair_details

    def get_price_for_pair(self, as_dict: bool = False):
        """
        Pull prices for pair from the respective API
        """
        price = self._price_for_pair()
        if as_dict:
            return price.to_dict('list')
        return price

    def get_orderbook_for_pair(self, as_dict=False):
        """
        Pull order book data for pair
        """
        market_id, timestamp, bid_price, bid_qty, ask_price, ask_qty = self._orderbook_for_pair()
        orderbook = pd.DataFrame({
            "market_id": market_id,
            "timestamp": timestamp,
            "bid_price": bid_price,
            "bid_qty": bid_qty,
            "ask_price": ask_price,
            "ask_qty": ask_qty
        })

        if as_dict:
            return orderbook.to_dict('list')
        return orderbook

    @staticmethod
    def _coins_tradeable_url():
        req_url = BTCMarkets.BASE_URL + '/markets'
        return req_url

    @staticmethod
    def _coins_tradeable(replace=True):
        url = BTCMarkets._coins_tradeable_url()
        coins_tradeable = pd.read_json(url)
        if replace:
            coins_tradeable["marketId"] = coins_tradeable["marketId"].str.replace("-", "_")
        return coins_tradeable

    def _check_currency_exists(self):
        coins_tradeable = BTCMarkets._coins_tradeable(replace=True)
        if self.market_id.replace("-", "_") not in coins_tradeable["marketId"].tolist():
            raise ValueError(f"Pair {self.market_id} does not exist in BTCMarkets")

    def _details_for_pair(self):
        coins_tradeable = BTCMarkets._coins_tradeable(replace=False)
        pair_details = coins_tradeable[coins_tradeable["marketId"] == self.market_id].copy(deep=True)
        pair_details["exchange_obj"] = BTCMarkets
        pair_details["marketId"] = pair_details["marketId"].str.replace("-", "_")
        return pair_details[["marketId", "baseAssetName", "quoteAssetName", "exchange_obj"]].reset_index(drop=True)

    def _price_for_pair_url(self):
        req_url = BTCMarkets.BASE_URL + f'/markets/{self.market_id}/ticker'
        return req_url

    def _price_for_pair(self):
        req_url = self._price_for_pair_url()
        req = requests.get(req_url)
        price = pd.json_normalize(json.loads(req.text))
        price["marketId"] = self.market_id
        price["timestamp"] = pd.to_datetime(datetime.utcnow())
        price = price.astype({
            "bestBid": float,
            "bestAsk": float,
            "lastPrice": float,
            "volume24h": float,
            "volumeQte24h": float,
            "price24h": float,
            "pricePct24h": float,
            "low24h": float,
            "high24h": float
        })
        price["marketId"] = price["marketId"].str.replace("-", "_")
        return price[["marketId", "bestBid", "bestAsk", "timestamp"]]

    def _orderbook_for_pair_url(self):
        req_url = BTCMarkets.BASE_URL + f'/markets/{self.market_id}/orderbook'
        return req_url

    def _orderbook_for_pair(self):
        req_url = self._orderbook_for_pair_url()
        json_resp = json.loads(requests.get(req_url).text)
        timestamp = datetime.utcnow()
        ask_price = [float(row[0]) for row in json_resp["asks"]]
        ask_qty = [float(row[1]) for row in json_resp["asks"]]
        bid_price = [float(row[0]) for row in json_resp["bids"]]
        bid_qty = [float(row[1]) for row in json_resp["bids"]]
        return self.market_id.replace("-", "_"), timestamp, bid_price, bid_qty, ask_price, ask_qty

    @staticmethod
    def _validate_currency_pair(market_id: str):
        if "_" in market_id:
            if len(market_id.split("_")) != 2:
                raise ValueError("Currency pair should be of the format <Currency>_<Currency>")
            return market_id.replace("_", "-")
        else:
            raise ValueError("Currency pair should be of the format <Currency>_<Currency>")


if __name__ == "__main__":
    # coins_tradeable = BTCMarkets.get_coins_tradeable()
    # print(coins_tradeable)

    obj = BTCMarkets("BTC_AUD")

    btc_aud_df = obj.get_details_for_pair()
    btc_aud_dict = obj.get_details_for_pair(as_dict=True)
    print(btc_aud_df)
    print(btc_aud_dict)

    btc_aud_price = obj.get_price_for_pair()
    btc_aud_price_dict = obj.get_price_for_pair(as_dict=True)
    print(btc_aud_price)
    print(btc_aud_price_dict)

    btc_aud_ob = obj.get_orderbook_for_pair()
    btc_aud_ob_dict = obj.get_orderbook_for_pair(as_dict=True)
    print(btc_aud_ob)
    print(btc_aud_ob_dict)
