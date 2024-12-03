import pandas as pd

class Strategy_MA:
    def __init__(self,
                 data: pd.DataFrame,
                 window_slow=26,
                 window_fast=12):
        
        # algorithm implementation
        close_prices = data["Close"]
        ma_fast = close_prices.rolling(window=window_fast, min_periods=1).mean()
        ma_slow = close_prices.rolling(window=window_slow, min_periods=1).mean()

        data["MA_fast"] = ma_fast
        data["MA_slow"] = ma_slow

        # trading signals
        data["BuyCondition"] = ma_fast >= ma_slow
        data["SellCondition"] = ma_fast < ma_slow

        self._df = data
