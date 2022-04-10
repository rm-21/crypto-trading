import oandapyV20.endpoints.pricing as pricing
import pandas as pd
from oandapyV20 import API

pd.set_option('display.max_columns', 20)


class Oanda:
    BASE_URL = "https://api-fxpractice.oanda.com"
    ACCESS_TOKEN = "a172c4339822eeecda7f3b6e7ffd9cf4-481ffa1101fd0ffea2e9364697c3283f"
    ACCOUNT_ID = "101-011-22118203-001"

    # print(client.request(pricing.PricingInfo(accountID, params={"instruments": "AUD_SGD"})))

    def __init__(self):
        self.client = API(access_token=Oanda.ACCESS_TOKEN)

    @staticmethod
    def get_details_for_pair(market_id: str, as_dict: bool = False):
        """
        Get the base and quote currencies
        """
        pair_details = Oanda._details_for_pair(market_id=market_id)
        if as_dict:
            return pair_details.to_dict(orient='list')
        return pair_details

    @staticmethod
    def get_price_for_pair(market_id: str, as_dict: bool = False):
        """
        Pull prices for pair from the respective API
        """
        price = Oanda._price_for_pair(market_id)
        if as_dict:
            return price.to_dict('list')
        return price

    @staticmethod
    def get_orderbook_for_pair(market_id: str, as_dict=False):
        """
        Pull order book data for pair
        """
        bid_price, bid_qty, ask_price, ask_qty = Oanda._orderbook_for_pair(market_id=market_id)
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
    def _details_for_pair(market_id: str):
        market_id = Oanda._validate_currency_pair(market_id)
        # Local scoped object
        obj_scoped = Oanda()
        obj_req = obj_scoped.client.request(pricing.PricingInfo(Oanda.ACCOUNT_ID,
                                                                params={"instruments": f"{market_id}"}))
        market_id = obj_req['prices'][0]['instrument']

        pair_details = pd.DataFrame({
            "marketId": market_id,
            "baseAssetName": market_id.split("_")[0],
            "quoteAssetName": market_id.split("_")[1]
        }, index=[0])
        return pair_details

    @staticmethod
    def _price_for_pair(market_id: str):
        market_id = Oanda._validate_currency_pair(market_id)

        # Local scoped object
        obj_scoped = Oanda()
        pair_details = obj_scoped.client.request(
            pricing.PricingInfo(Oanda.ACCOUNT_ID, params={"instruments": f"{market_id}"}))['prices'][0]

        base, quote = market_id.split("_")[0], market_id.split("_")[1]
        price = pd.DataFrame({
            "marketId": market_id,
            "bestBid": pair_details["bids"][0]['price'],
            "bestAsk": pair_details["asks"][0]['price'],
            "timestamp": pair_details["time"]
        }, index=[0])

        price["timestamp"] = pd.to_datetime(price["timestamp"])
        price = price.astype({
            "bestBid": float,
            "bestAsk": float,
        })
        return price

    @staticmethod
    def _orderbook_for_pair(market_id: str):
        market_id = Oanda._validate_currency_pair(market_id)

        # Local scoped object
        obj_scoped = Oanda()
        pair_details = obj_scoped.client.request(
            pricing.PricingInfo(Oanda.ACCOUNT_ID, params={"instruments": f"{market_id}"}))['prices'][0]

        ask_price = [float(x['price'])for x in pair_details["asks"]]
        ask_qty = [float(x['liquidity'])for x in pair_details["asks"]]
        bid_price = [float(x['price'])for x in pair_details["bids"]]
        bid_qty = [float(x['liquidity'])for x in pair_details["bids"]]
        return bid_price, bid_qty, ask_price, ask_qty

    @staticmethod
    def _validate_currency_pair(market_id: str):
        if "_" in market_id:
            if len(market_id.split("_")) != 2:
                raise ValueError("Currency pair should be of the format <Currency>_<Currency>")
            return market_id
        else:
            raise ValueError("Currency pair should be of the format <Currency>_<Currency>")


if __name__ == "__main__":
    # aud_sgd_details = Oanda.get_details_for_pair("AUD_SGD")
    # aud_sgd_details_dict = Oanda.get_details_for_pair("AUD_SGD", as_dict=True)
    # print(aud_sgd_details_dict)

    # aud_sgd_price = Oanda.get_price_for_pair("AUD_SGD")
    # aud_sgd_price_dict = Oanda.get_price_for_pair("AUD_SGD", as_dict=True)
    # print(aud_sgd_price)

    btc_aud_ob = Oanda.get_orderbook_for_pair("AUD_SGD")
    btc_aud_ob_dict = Oanda.get_orderbook_for_pair("AUD_SGD", as_dict=True)
    print(btc_aud_ob)
