from ta.momentum import RSIIndicator

from core.algo_core import AlgorithmDefinition
from core.yf_core import round_result

class Strategy(AlgorithmDefinition):
    def __init__(self, algorithmName, 
                 algo: AlgorithmDefinition, 
                 slow_window=26, 
                 fast_window=12, 
                 signal_window=9):
        self.algorithmName = algorithmName
        
        super().__init__(algo.data)

        # Strategy: Volume Weighted MACD crossover
        self.data["vol_price"] = self.data["Close"] * self.data["Volume"]
        
        self.data["slow_vw_macd"] = self.data["vol_price"].rolling(slow_window).sum() / self.data["Volume"]
        self.data["fast_vw_macd"] = self.data["vol_price"].rolling(fast_window).sum() / self.data["Volume"]
        
        self.data["macd"] = self.data["fast_vw_macd"] - self.data["slow_vw_macd"]
        self.data["macd_signal"] = self.data["vol_price"].rolling(signal_window).sum() / self.data["Volume"]
        self.data["macd_diff"] = self.data["macd"] - self.data["macd_signal"]

        # Algo: Generate trading signals
        self.data['BuyCondition'] = self.data["macd_diff"] > 0
        self.data['SellCondition'] = self.data["macd_diff"] < 0
