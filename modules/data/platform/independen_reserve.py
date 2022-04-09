import pandas as pd
import requests
import json
pd.set_option('display.max_columns', 20)


class IndependentReserve:
    BASE_URL = "https://api.independentreserve.com/Public"

    @staticmethod
    def get_coins_tradeable():
        """
        List of possible tradeable pairs: <Currency>_<Currency>
        """
        coins_tradeable = IndependentReserve._coins_tradeable()
        return coins_tradeable

    @staticmethod
    def get_details_for_pair(market_id: str, as_dict: bool = False):
        """
        Get the base and quote currencies
        """
        pair_details = IndependentReserve._details_for_pair(market_id=market_id)
        if as_dict:
            return pair_details.to_dict(orient='list')
        return pair_details

    @staticmethod
    def get_price_for_pair(market_id: str, as_dict: bool = False):
        """
        Pull prices for pair from the respective API
        """
        price = IndependentReserve._price_for_pair(market_id)
        if as_dict:
            return price.to_dict('list')
        return price

    @staticmethod
    def get_orderbook_for_pair(market_id: str, as_dict = False):
        """
        Pull order book data for pair
        """
        bid_price, bid_qty, ask_price, ask_qty = IndependentReserve._orderbook_for_pair(market_id=market_id)
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

    @staticmethod
    def _details_for_pair(market_id: str):
        pair_details = pd.DataFrame()
        coins_tradeable = IndependentReserve._coins_tradeable()
        if market_id in coins_tradeable:
            pair_details = pd.DataFrame({
                "marketId": market_id,
                "baseAssetName": market_id.split("_")[0],
                "quoteAssetName": market_id.split("_")[1]
            }, index=[0])
        return pair_details

    @staticmethod
    def _price_for_pair(market_id: str):
        market_id = IndependentReserve._validate_currency_pair(market_id)
        base, quote = market_id.split("-")[0].capitalize(), market_id.split("-")[1]

        req_url = IndependentReserve.BASE_URL + f'/GetMarketSummary?primaryCurrencyCode={base}&secondaryCurrencyCode={quote}'
        req = requests.get(req_url)
        price = pd.json_normalize(json.loads(req.text))

        price = pd.DataFrame({
            "marketId": market_id,
            "bestBid": price["CurrentHighestBidPrice"],
            "bestAsk": price["CurrentLowestOfferPrice"],
            "lastPrice": price["LastPrice"],
            "volume24h": price[f"DayVolume{base}"],
            "volumeQte24h": price[f"DayVolume{base}InSecondaryCurrrency"],
            "price24h": price["DayAvgPrice"],
            "low24h": price["DayLowestPrice"],
            "high24h": price["DayHighestPrice"],
            "timestamp": price["CreatedTimestampUtc"]
        })

        price["timestamp"] = pd.to_datetime(price["timestamp"])
        price = price.astype({
            "bestBid": float,
            "bestAsk": float,
            "lastPrice": float,
            "volume24h": float,
            "volumeQte24h": float,
            "price24h": float,
            "low24h": float,
            "high24h": float
        })

        return price[["marketId", "bestBid", "bestAsk", "timestamp"]]

    @staticmethod
    def _orderbook_for_pair(market_id: str):
        market_id = IndependentReserve._validate_currency_pair(market_id)
        base, quote = market_id.split("-")[0], market_id.split("-")[1]
        req_url = IndependentReserve.BASE_URL + f'/GetOrderBook?primaryCurrencyCode={base}&secondaryCurrencyCode={quote}'
        json_resp = json.loads(requests.get(req_url).text)
        ask_price = [float(x["Price"]) for x in json_resp["BuyOrders"]][:50]
        ask_qty = [float(x["Volume"] )for x in json_resp["BuyOrders"]][:50]
        bid_price = [float(x["Price"]) for x in json_resp["SellOrders"]][:50]
        bid_qty = [float(x["Volume"]) for x in json_resp["SellOrders"]][:50]
        return ask_price, ask_qty, bid_price, bid_qty

    @staticmethod
    def _validate_currency_pair(market_id: str):
        if "_" in market_id:
            if len(market_id.split("_")) != 2:
                raise ValueError("Currency pair should be of the format <Currency>_<Currency>")
            return market_id.replace("_", "-")
        else:
            raise ValueError("Currency pair should be of the format <Currency>_<Currency>")


if __name__ == "__main__":
    # coins_trade = IndependentReserve.get_coins_tradeable()
    # print(coins_trade)

    # btc_sgd_df = IndependentReserve.get_details_for_pair("XBT_SGD")
    # btc_sgd_dict = IndependentReserve.get_details_for_pair("XBT_SGD", as_dict=True)
    # print(btc_sgd_df)

    # btc_sgd_price = IndependentReserve.get_price_for_pair("XBT_SGD")
    # btc_sgd_price_dict = IndependentReserve.get_price_for_pair("XBT_SGD", as_dict=True)
    # print(btc_sgd_price)

    btc_aud_ob = IndependentReserve.get_orderbook_for_pair("BTC_AUD")
    btc_aud_ob_dict = IndependentReserve.get_orderbook_for_pair("BTC_AUD", as_dict=True)
    print(btc_aud_ob.info())
