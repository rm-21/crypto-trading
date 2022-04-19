# Crypto Trading Bot

## Triangular Arbitrage in Crypto Exchanges

The project aims to implement a triangular arbitrage strategy. It currently is limited only to the Australian crypto 
exchanges. The arbitrage is as follows:

## Sample Analysis of the `AUD`, `SGD`, `XRP` trio
[Link to the Analysis](https://github.com/rm-21/crypto-trading/blob/main/analysis/trade_analysis_XRP.ipynb) 

## How to Run
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

## Currency Pairs
* Fiat (traditional) currency - *AUD* - Australian Dollar
* Fiat (traditional) currency - *Any* - Like *SGD*, *USD*, etc.
* Cryptocurrency - *Any* - Like *BTC*, *ETH*, etc.

## Currency Format
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

### Step 1:
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

### Step 2
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

### Step 3
**Arbitrage Opportunity:**<br>
With the above price dataframe, we now have all the information for an arbitrage.<br>

**Method `get_trade_logs`**:
This method does many things in a step-wise manner to simulate and check for an arbitrage opportunity. Let us go through
all of them:

1. **Conversion Direction**: It creates a cyclic graph, with edges as the currency in each pair. The `get_paths` method
in `conversion_direction.py` outputs the following result: 
```python
paths = [['AUD', 'BTC', 'SGD', 'AUD'], ['AUD', 'SGD', 'BTC', 'AUD']]
```
What this shows if you initially have AUD and want to do an arbitrage, you have two ways to do it:
* **Path1**: AUD --> BTC --> SGD --> AUD
* **Path2**: AUD --> SGD --> BTC --> AUD

2. **Conversion Params**: Depending on the currency pair we have, a list of dictionaries, containing the conversion rate and direction, as 
follows will be created:
```python
quotes_to_use = [
    [{'ask': 53996.2,
   'base_currency': 'BTC',
   'bid': 53862.7,
   'direction': 'reverse',
   'quote_currency': 'AUD'},
  {'ask': 54817.71,
   'base_currency': 'BTC',
   'bid': 54611.82,
   'direction': 'forward',
   'quote_currency': 'SGD'},
  {'ask': 1.01521,
   'base_currency': 'AUD',
   'bid': 1.0151,
   'direction': 'reverse',
   'quote_currency': 'SGD'}],
 [{'ask': 1.01521,
   'base_currency': 'AUD',
   'bid': 1.0151,
   'direction': 'forward',
   'quote_currency': 'SGD'},
  {'ask': 54817.71,
   'base_currency': 'BTC',
   'bid': 54611.82,
   'direction': 'reverse',
   'quote_currency': 'SGD'},
  {'ask': 53996.2,
   'base_currency': 'BTC',
   'bid': 53862.7,
   'direction': 'forward',
   'quote_currency': 'AUD'}]
]
```

3. **Conversion**: The items in `quotes_to_use` list will be passed as params to the function `currency_conversion` in
`conversion.py` module. The function calculates the correct swap rate based on the `direction` parameter.<br><br>
If you look carefully, each dictionary in the first list is a single iteration or conversion.<br><br>
Using that as a reference, we calculate the potential profit/loss for each of the two paths in point 1, as if the trade 
was taken. The details are added to the `TRADES_LOG` variable of the object, which is the output of the `get_trade_logs`
method.


### Step 4
The output trades log gets saved along with the prices in a separate local folder of your choice using the 
`save_price_trade` function. In addition, any profitable opportunity when identified gets printed out to the console.
<br><br>**Example Trade Logs:**<br>

| index    | new_amount    | denomination | swap_rate    | direction  | profit      | percent   |
|----------|---------------|--------------|--------------|------------|-------------|-----------|
| 0_trade1 | 1.846431      | BTC          | 0.000018     | AUD to BTC | 0           | 0         |
| 0_trade2 | 101144.270349 | SGD          | 54778.250000 | BTC to SGD | 0           | 0         |
| 0_trade3 | 99690.778794  | AUD          | 0.985630     | SGD to AUD | -309.221206 | -0.003092 |
| 1_trade1 | 101447.000000 | SGD          | 1.014470     | AUD to SGD | 0           | 0         |
| 1_trade2 | 1.844609      | BTC          | 0.000018     | SGD to BTC | 0           | 0         |
| 1_trade3 | 99709.710385  | AUD          | 54054.660000 | BTC to AUD | -290.289615 | -0.002903 |

## Current Potential
1. You can add any exchange of your choice under `modules\data\platform`. Refer to any of the existing exchange codes
for the class schema. If consistent, then you can run the arbitrage with the exchange of your choice, by modifying the 
`currency_dict`.
2. You can trade any pair in the current exchanges by simply modifying the currencies in `currency_dict`. Errors will be
raised if currencies don't exist or are not tradeable. 
3. The code is scalable as a scanner for arbitrage. Runs have revealed that when an opportunity arises, it stays from
30 seconds to a few minutes before being filled.

## Way Forward
1. Add support for exchanges that use the opposite currency format.
2. Reduce latency by using websockets. Currently, not added because, Independent Reserve websockets feed individual
changes in the orderbook and would require orderbook construction at specified intervals. The task was beyond the
current project scope.
3. Fetch round-off figures from the exchanges, to avoid order rejection issues in live mode (TBD).
4. Verify market depth for appropriate position sizing and avoiding extremely illiquid markets.