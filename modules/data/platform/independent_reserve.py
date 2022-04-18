import pandas as pd
import requests
import json
from datetime import datetime
pd.set_option('display.max_columns', 20)


class IndependentReserve:
    BASE_URL = "https://api.independentreserve.com/Public"

    def __init__(self, market_id: str):
        self.market_id = IndependentReserve._validate_currency_pair(market_id)
        self._check_currency_exists()

    @staticmethod
    def get_coins_tradeable():
        """
        List of possible tradeable pairs: <Currency>_<Currency>
        """
        coins_tradeable = IndependentReserve._coins_tradeable()
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
        req_url_primary_currency = IndependentReserve.BASE_URL + '/GetValidPrimaryCurrencyCodes'
        req_url_secondary_currency = IndependentReserve.BASE_URL + '/GetValidSecondaryCurrencyCodes'
        return req_url_primary_currency, req_url_secondary_currency

    @staticmethod
    def _coins_tradeable():
        url = IndependentReserve._coins_tradeable_url()
        primary_currency = json.loads(requests.get(url[0]).text)
        secondary_currency = json.loads(requests.get(url[1]).text)
        coins_tradeable = ["_".join([base, quote]).upper()
                           for base in primary_currency
                           for quote in secondary_currency]
        return coins_tradeable

    def _check_currency_exists(self):
        coins_tradeable = IndependentReserve._coins_tradeable()
        if self.market_id not in coins_tradeable:
            raise ValueError(f"Pair {self.market_id} does not exist in IndependentReserve.")

    def _replace_XBT_with_BTC(self):
        market_id = ""
        if self.market_id.split("_")[0] == "XBT":
            market_id = "BTC" + "_" + self.market_id.split("_")[1]
        elif self.market_id.split("_")[1] == "XBT":
            market_id = self.market_id.split("_")[0] + "_" + "BTC"
        else:
            market_id = self.market_id
        return market_id

    def _details_for_pair(self):
        market_id = self._replace_XBT_with_BTC()
        pair_details = pd.DataFrame({
            "marketId": market_id,
            "baseAssetName": market_id.split("_")[0],
            "quoteAssetName": market_id.split("_")[1],
            "exchange_obj": IndependentReserve
        }, index=[0])
        return pair_details

    def _price_for_pair_url(self):
        base, quote = self.market_id.split("_")[0].capitalize(), self.market_id.split("_")[1]
        req_url = IndependentReserve.BASE_URL + f'/GetMarketSummary?primaryCurrencyCode={base}&secondaryCurrencyCode={quote}'
        return req_url, base, quote

    def _price_for_pair(self):
        req_url, base, quote = self._price_for_pair_url()
        req = requests.get(req_url)
        price = pd.json_normalize(json.loads(req.text))
        market_id = self._replace_XBT_with_BTC()
        price = pd.DataFrame({
            "marketId": market_id,
            "bestBid": float(price["CurrentHighestBidPrice"]),
            "bestAsk": float(price["CurrentLowestOfferPrice"]),
            "lastPrice": float(price["LastPrice"]),
            "volume24h": float(price[f"DayVolumeXbt"]),
            "volumeQte24h": float(price[f"DayVolumeXbtInSecondaryCurrrency"]),
            "price24h": float(price["DayAvgPrice"]),
            "low24h": float(price["DayLowestPrice"]),
            "high24h": float(price["DayHighestPrice"]),
            "timestamp": pd.to_datetime(datetime.utcnow())
        }, index=[0])

        return price[["marketId", "bestBid", "bestAsk", "timestamp"]]

    def _orderbook_for_pair_url(self):
        base, quote = self.market_id.split("_")[0], self.market_id.split("_")[1]
        req_url = IndependentReserve.BASE_URL + f'/GetOrderBook?primaryCurrencyCode={base}&secondaryCurrencyCode={quote}'
        return req_url, base, quote

    def _orderbook_for_pair(self):
        req_url, base, quote = self._orderbook_for_pair_url()
        json_resp = json.loads(requests.get(req_url).text)
        timestamp = datetime.utcnow()
        ask_price = [float(x["Price"]) for x in json_resp["BuyOrders"]][:50]
        ask_qty = [float(x["Volume"]) for x in json_resp["BuyOrders"]][:50]
        bid_price = [float(x["Price"]) for x in json_resp["SellOrders"]][:50]
        bid_qty = [float(x["Volume"]) for x in json_resp["SellOrders"]][:50]
        market_id = self._replace_XBT_with_BTC()
        return market_id, timestamp, ask_price, ask_qty, bid_price, bid_qty

    @staticmethod
    def _validate_currency_pair(market_id: str):
        if "_" in market_id:
            if len(market_id.split("_")) != 2:
                raise ValueError("Currency pair should be of the format <Currency>_<Currency>")
            if market_id.split("_")[0] == "BTC":
                market_id = "XBT" + "_" + market_id.split("_")[1]
            elif market_id.split("_")[1] == "BTC":
                market_id = market_id.split("_")[0] + "_" + "XBT"
            return market_id
        else:
            raise ValueError("Currency pair should be of the format <Currency>_<Currency>")


if __name__ == "__main__":
    # coins_trade = IndependentReserve.get_coins_tradeable()
    # print(coins_trade)

    obj = IndependentReserve("BTC_SGD")
    # obj = IndependentReserve("ETH_USD")

    btc_sgd_df = obj.get_details_for_pair()
    btc_sgd_dict = obj.get_details_for_pair(as_dict=True)
    print(btc_sgd_df)
    print(btc_sgd_dict)

    btc_sgd_price = obj.get_price_for_pair()
    btc_sgd_price_dict = obj.get_price_for_pair(as_dict=True)
    print(btc_sgd_price)
    print(btc_sgd_price_dict)

    btc_aud_ob = obj.get_orderbook_for_pair()
    btc_aud_ob_dict = obj.get_orderbook_for_pair(as_dict=True)
    print(btc_aud_ob)
    print(btc_aud_ob_dict)
