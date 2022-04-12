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
Let us walk through the code keeping the `trading_bot.py` file as a reference.
