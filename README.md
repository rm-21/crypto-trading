# Crypto Trading Bot

## Triangular Arbitrage in Crypto Exchanges

The project aims to implement a triangular arbitrage strategy. It currently is limited only to the Australian crypto 
exchanges. The arbitrage is as follows:

### How to Run
1. Clone the project on your local system.
2. Create a conda environment using the `.yml` file.
3. Navigate to `crypto-trading/app/trading_bot.py`
4. Under `__name__ == "__main__"` code block:
   1. Modify `cur_dict_<num>` with the currency pair and the respective exchange.
   2. Modify `run_surface_arb` function with:
      1. `init_amount`: amount you have in your held currency
      2. `init_cur`: your held currency
      3. `run_interval`: frequency of checking for an arbitrage opportunity. Has to be 1 second or more.
      4. `max_duration`: maximum number of times to check for arbitrage
      5. `path`: the path on your local system to store the log files
   3. Run the `trading_bot.py` file in a terminal or IDE of your choice.

### Currency Pairs
* Fiat (traditional) currency - *AUD* - Australian Dollar
* Fiat (traditional) currency - *Any* - Like *SGD*, *USD*, etc.
* Cryptocurrency - *Any* - Like *BTC*, *ETH*, etc.

### Currency Format
Any exchange that you use must have this quotes format: `BaseCurrency_QuoteCurrency`

## Code Flow
Let us walk through the code keeping the `run_surface_arb` function in `trading_bot.py`as a reference.

**Argument `currency_dict`**:<br>
```python
currency_dict = {
   "currency_pair1": ExchangObj1,
   "currency_pair2": ExchangObj2,
   "currency_pair3": ExchangObj3,
}
```

This parameter should contain the currency pair and the exchange on which the said pair trades. For example, BTC_SGD
trades on BTCMarkets.

**Step 1:**<br>
Initialise the `IdentifyPairs` object. When initialised, the following happens:
* **Exchange objects for each currency pair** that will help you pull the data for that pair get created.
  * Checks whether currency pair formats are valid or not.
  * Checks whether the said currency pair trades on the exchange or not.<br><br>
* **Method `get_tradeable_trio`**:

| marketId | baseAssetName | quoteAssetName | exchange_obj       |
| -------- |---------------|----------------|--------------------|
|AUD_SGD   | AUD           | SGD            | Oanda              |
|BTC_AUD   | BTC           | AUD            | BTCMarkets         |
|BTC_SGD   | BTC           | SGD            | IndependentReserve |

You get a `pandas` dataframe with the above details. The `exchange_obj` column contains the object from which data for 
each pair will be pulled.

**Step 2:**<br>
**Price for Trio**: With these details, you pass them to the `Data` object. The object has a method `get_price_for_trio`, which pulls the price for each pair using a `ThreadPoolExecutor`. It acts as an API, so that you don't have to call the prices for each pair individually. Under the hood, it is using the `get_price_for_pair` method for each currency pair.
It returns the following dataframe:

| marketId | bestBid     | bestAsk     | timestamp                  |
| -------- |-------------|-------------|----------------------------|
|AUD_SGD   | 1.01495     | 1.01506     | 2022-04-12 05:22:49.901788 |
|BTC_AUD   | 53828.51000 | 53912.55000 | 2022-04-12 05:22:50.083840 |
|BTC_SGD   | 54557.74000 | 54780.44000 | 2022-04-12 05:22:51.523414 |

The dataframe is self-explanatory. The timestamp is in UTC and specifies the time when the price for a pair was called
and stored. The difference in seconds and milliseconds that you see is because of two reasons:
- `ThreadPoolExecutor`: Is not a substitute for parallel computing. It just optimises the resources.
- `IndependentReserve`: The independent reserve exchange API is slightly slower than that of Oanda and BTCMarkets.

**Step 3:**<br>
**Arbitrage Opportunity:**<br>
With the above price dataframe, we now have all the information for an arbitrage.
