from ta.trend import MACD

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

        # Strategy: MACD crossover
        # macd        : EMA(Shorter Period) - EMA(Longer Period)
        # macd_signal : EMA(MACD, 9 days)
        # macd_diff   : macd - macd_signal
        
        macd_obj = MACD(close=self.data["Close"], 
                        window_slow=slow_window,
                        window_fast=fast_window,
                        window_sign=signal_window)
        
        self.data["macd"] = round_result(macd_obj.macd())
        self.data["macd_signal"] = round_result(macd_obj.macd_signal())
        self.data["macd_diff"] = round_result(macd_obj.macd_diff())

        # Algo: Generate trading signals
        self.data['BuyCondition'] = self.data["macd_diff"] < 0
        self.data['SellCondition'] = self.data["macd_diff"] > 0
