import oandapyV20.endpoints.pricing as pricing
import pandas as pd
from oandapyV20 import API
from datetime import datetime
from modules.data.oanda_login import oanda_login

pd.set_option('display.max_columns', 20)


class Oanda:
    BASE_URL = "https://api-fxpractice.oanda.com"
    ACCESS_TOKEN = oanda_login["ACCESS_TOKEN"]
    ACCOUNT_ID = oanda_login["ACCOUNT_ID"]

    def __init__(self, market_id: str):
        self.client = API(access_token=Oanda.ACCESS_TOKEN)
        self.market_id = Oanda._validate_currency_pair(market_id)

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

    def _details_for_pair(self):
        obj_req = self.client.request(pricing.PricingInfo(Oanda.ACCOUNT_ID,
                                                          params={"instruments": f"{self.market_id}"}))
        market_id = obj_req['prices'][0]['instrument']

        pair_details = pd.DataFrame({
            "marketId": market_id,
            "baseAssetName": market_id.split("_")[0],
            "quoteAssetName": market_id.split("_")[1],
            "exchange_obj": Oanda
        }, index=[0])
        return pair_details

    def _price_for_pair(self):
        pair_details = self.client.request(
            pricing.PricingInfo(Oanda.ACCOUNT_ID, params={"instruments": f"{self.market_id}"}))['prices'][0]

        base, quote = self.market_id.split("_")[0], self.market_id.split("_")[1]
        price = pd.DataFrame({
            "marketId": self.market_id,
            "bestBid": pair_details["bids"][0]['price'],
            "bestAsk": pair_details["asks"][0]['price'],
            "timestamp": pd.to_datetime(datetime.utcnow())
        }, index=[0])

        price["timestamp"] = pd.to_datetime(price["timestamp"])
        price = price.astype({
            "bestBid": float,
            "bestAsk": float,
        })
        return price

    def _orderbook_for_pair(self):
        pair_details = self.client.request(
            pricing.PricingInfo(Oanda.ACCOUNT_ID, params={"instruments": f"{self.market_id}"}))['prices'][0]
        timestamp = datetime.utcnow()
        ask_price = [float(x['price']) for x in pair_details["asks"]]
        ask_qty = [float(x['liquidity']) for x in pair_details["asks"]]
        bid_price = [float(x['price']) for x in pair_details["bids"]]
        bid_qty = [float(x['liquidity']) for x in pair_details["bids"]]
        return self.market_id, timestamp, bid_price, bid_qty, ask_price, ask_qty

    @staticmethod
    def _validate_currency_pair(market_id: str):
        if "_" in market_id:
            if len(market_id.split("_")) != 2:
                raise ValueError("Currency pair should be of the format <Currency>_<Currency>")
            return market_id
        else:
            raise ValueError("Currency pair should be of the format <Currency>_<Currency>")


if __name__ == "__main__":
    obj = Oanda("AUD_SGD")

    aud_sgd_details = obj.get_details_for_pair()
    aud_sgd_details_dict = obj.get_details_for_pair(as_dict=True)
    print(aud_sgd_details)
    print(aud_sgd_details_dict)

    aud_sgd_price = obj.get_price_for_pair()
    aud_sgd_price_dict = obj.get_price_for_pair(as_dict=True)
    print(aud_sgd_price)
    print(aud_sgd_price_dict)

    btc_aud_ob = obj.get_orderbook_for_pair()
    btc_aud_ob_dict = obj.get_orderbook_for_pair(as_dict=True)
    print(btc_aud_ob)
    print(btc_aud_ob_dict)
