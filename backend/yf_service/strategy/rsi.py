import pandas as pd
from ta.momentum import RSIIndicator


class Strategy_RSI:
    def __init__(self,
                 data: pd.DataFrame,
                 window_slow=14,
                 window_fast=2):
        
        # algorithm implementation
        close_prices = data["Close"]
        rsi_slow = RSIIndicator(close=close_prices, window=window_slow).rsi()
        rsi_fast = RSIIndicator(close=close_prices, window=window_fast).rsi()

        data["rsi_slow"] = rsi_slow
        data["rsi_fast"] = rsi_fast

        # trading signals
        data["BuyCondition"]  = data["rsi_fast"] > data["rsi_slow"]
        data["SellCondition"] = data["rsi_fast"] < data["rsi_slow"]

        self._df = data
