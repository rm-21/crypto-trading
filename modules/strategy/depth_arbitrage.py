from surface_arb import SurfaceArb


class DepthArb(SurfaceArb):
    def __init__(
        self, trio: list, trio_prices: dict, init_amount: float, init_currency: str
    ):
        super().__init__(trio, trio_prices, init_amount, init_currency)
        DepthArb.TRADES_LOG = self.get_trade_logs
