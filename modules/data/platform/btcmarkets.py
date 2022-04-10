import pandas as pd
import requests
import json
pd.set_option('display.max_columns', 20)


class BTCMarkets:
    BASE_URL = "https://api.btcmarkets.net/v3"

    @staticmethod
    def get_coins_tradeable():
        """
        List of possible tradeable pairs: <Currency>_<Currency>
        """
        coins_tradeable = BTCMarkets._coins_tradeable()
        return coins_tradeable

    @staticmethod
    def get_details_for_pair(market_id: str, as_dict: bool = False):
        """
        Get the base and quote currencies
        """
        pair_details = BTCMarkets._details_for_pair(market_id=market_id)
        if as_dict:
            return pair_details.to_dict(orient='list')
        return pair_details

    @staticmethod
    def get_price_for_pair(market_id: str, as_dict: bool = False):
        """
        Pull prices for pair from the respective API
        """
        price = BTCMarkets._price_for_pair(market_id)
        if as_dict:
            return price.to_dict('list')
        return price

    @staticmethod
    def get_orderbook_for_pair(market_id: str, as_dict=False):
        """
        Pull order book data for pair
        """
        bid_price, bid_qty, ask_price, ask_qty = BTCMarkets._orderbook_for_pair(market_id=market_id)
        orderbook = pd.DataFrame({
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

    @staticmethod
    def _check_currency_exists(market_id: str):
        market_id = BTCMarkets._validate_currency_pair(market_id)
        coins_tradeable = BTCMarkets._coins_tradeable(replace=False)
        if market_id not in coins_tradeable["marketId"].tolist():
            raise ValueError(f"Pair {market_id} does not exist in BTCMarkets")

    @staticmethod
    def _details_for_pair(market_id: str):
        BTCMarkets._check_currency_exists(market_id)
        coins_tradeable = BTCMarkets._coins_tradeable()
        pair_details = coins_tradeable[coins_tradeable["marketId"] == market_id].copy(deep=True)
        return pair_details[["marketId", "baseAssetName", "quoteAssetName"]].reset_index(drop=True)

    @staticmethod
    def _price_for_pair_url(market_id: str):
        BTCMarkets._check_currency_exists(market_id)
        market_id = BTCMarkets._validate_currency_pair(market_id)
        req_url = BTCMarkets.BASE_URL + f'/markets/{market_id}/ticker'
        return req_url

    @staticmethod
    def _price_for_pair(market_id: str):
        req_url = BTCMarkets._price_for_pair_url(market_id)
        req = requests.get(req_url)
        price = pd.json_normalize(json.loads(req.text))
        price["marketId"] = market_id
        price["timestamp"] = pd.to_datetime(price["timestamp"])
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
        return price[["marketId", "bestBid", "bestAsk", "timestamp"]]

    @staticmethod
    def _orderbook_for_pair_url(market_id: str):
        BTCMarkets._check_currency_exists(market_id)
        market_id = BTCMarkets._validate_currency_pair(market_id)
        req_url = BTCMarkets.BASE_URL + f'/markets/{market_id}/orderbook'
        return req_url

    @staticmethod
    def _orderbook_for_pair(market_id: str):
        req_url = BTCMarkets._orderbook_for_pair_url(market_id)
        json_resp = json.loads(requests.get(req_url).text)
        ask_price = [float(row[0]) for row in json_resp["asks"]]
        ask_qty = [float(row[1]) for row in json_resp["asks"]]
        bid_price = [float(row[0]) for row in json_resp["bids"]]
        bid_qty = [float(row[1]) for row in json_resp["bids"]]
        return bid_price, bid_qty, ask_price, ask_qty

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

    # btc_aud_df = BTCMarkets.get_details_for_pair("BTC_AUD")
    # btc_aud_dict = BTCMarkets.get_details_for_pair("BTC_AUD", as_dict=True)
    # print(btc_aud_df)

    # btc_aud_price = BTCMarkets.get_price_for_pair("BTC_AUD")
    # btc_aud_price_dict = BTCMarkets.get_price_for_pair("BTC_AUD", as_dict=True)
    # print(btc_aud_price)

    btc_aud_ob = BTCMarkets.get_orderbook_for_pair("BTC_AUD")
    btc_aud_ob_dict = BTCMarkets.get_orderbook_for_pair("BTC_AUD", as_dict=True)
    print(btc_aud_ob)
