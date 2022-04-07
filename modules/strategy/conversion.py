class Conversion:
    @staticmethod
    def currency_conversion(
        init_amount: float,
        base_currency: str,
        quote_currency: str,
        bid: float,
        ask: float,
        direction: str,
    ):
        if direction == "forward":
            _base_cur = base_currency
            _quote_cur = quote_currency
            _swap_rate = 1 / ask

            return {
                "new_amount": _swap_rate * init_amount,
                "denomination": _quote_cur,
                "swap_rate": _swap_rate,
                "direction": f"{_base_cur} to {_quote_cur}",
            }

        elif direction == "reverse":
            _base_cur = quote_currency
            _quote_cur = base_currency
            _swap_rate = bid

            return {
                "new_amount": _swap_rate * init_amount,
                "denomination": _quote_cur,
                "swap_rate": _swap_rate,
                "direction": f"{_base_cur} to {_quote_cur}",
            }

        else:
            return ValueError(
                "Invalid direction of conversion. Please pass `forward` or `reverse`"
            )
