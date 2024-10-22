import pandas as pd


class Strategy_VW_MACD:
    def __init__(self, 
                 data: pd.DataFrame,
                 window_slow=26, 
                 window_fast=12,
                 window_signal=9):
        
        # algorithm implementation
        close_prices = data["Close"]
        volume = data["Volume"]
        volume_weighted_price = close_prices * volume

        slow_vw_macd = self._ema(volume_weighted_price / volume, window_slow)
        fast_vw_macd = self._ema(volume_weighted_price / volume, window_fast)

        macd_diff = fast_vw_macd - slow_vw_macd
        macd_signal = self._ema(macd_diff, window_signal)

        data["VW_MACD"] = macd_diff
        data["VW_MACD_signal"] = macd_signal
        data["VW_MACD_diff"] = macd_diff - macd_signal

        # trading signals
        data["BuyCondition"] = (data["VW_MACD_diff"] > 0) & (data["VW_MACD_diff"].shift(1) <= 0)
        data["SellCondition"] = (data["VW_MACD_diff"] < 0) & (data["VW_MACD_diff"].shift(1) >= 0)

        self._df = data

    @staticmethod
    def _ema(close, window):
        return close.ewm(span=window, adjust=False).mean()
