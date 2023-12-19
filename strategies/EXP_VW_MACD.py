from ta.trend import ema_indicator

import pandas as pd
from core.algo_core import AlgorithmDefinition

class Strategy(AlgorithmDefinition):
    def __init__(self, algorithmName, algo: AlgorithmDefinition, fast_line, slow_line, signal_line=9):
        self.algorithmName = algorithmName
        self.fast_line = fast_line
        self.slow_line = slow_line
        
        super().__init__(algo.data)

        # Strategy: Volume Weighted MACD crossover
        self.data["vol_price"] = self.data["Close"] * self.data["Volume"]
        
        self.data["slow_vw_macd"] = self.calculate_ema(self.data["vol_price"].rolling(slow_line).sum() / self.data["Volume"], slow_line)
        self.data["fast_vw_macd"] = self.calculate_ema(self.data["vol_price"].rolling(fast_line).sum() / self.data["Volume"], fast_line)
        self.data["macd_signal"] = self.calculate_ema(self.data["vol_price"].rolling(signal_line).sum() / self.data["Volume"], signal_line)
        
        self.data["macd_line"] = (self.data["slow_vw_macd"] - self.data["fast_vw_macd"]) - self.data["macd_signal"]

        # Algo: Generate trading signals
        self.data['BuyCondition'] = self.data["macd_line"] > 0
        self.data['SellCondition'] = self.data["macd_line"] < 0

    @staticmethod
    def calculate_ema(series, span):
        return ema_indicator(series, span)
