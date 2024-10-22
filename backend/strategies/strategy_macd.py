import pandas as pd
from ta.trend import MACD


class Strategy_MACD:
    def __init__(self,
                 data: pd.DataFrame,
                 window_slow=26,
                 window_fast=12,
                 window_signal=9):
        
        # algorithm implementation
        close_prices = data["Close"]
        macd_obj = MACD(
            close=close_prices,
            window_slow=window_slow,
            window_fast=window_fast,
            window_sign=window_signal,
        )

        data["macd"] = macd_obj.macd()
        data["macd_signal"] = macd_obj.macd_signal()
        data["macd_diff"] = macd_obj.macd_diff()

        # trading signals
        data["BuyCondition"] = (data["macd_diff"] > 0) & (data["macd_diff"].shift(1) <= 0)
        data["SellCondition"] = (data["macd_diff"] < 0) & (data["macd_diff"].shift(1) >= 0)

        self._df = data

    def get_signals(self):
        return self._df[["macd", "macd_signal", "macd_diff", "BuySignal", "SellSignal"]]
