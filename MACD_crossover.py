from ta.trend import MACD

from algo_core import AlgorithmDefinition
from core import round_result

class Strategy(AlgorithmDefinition):
    def __init__(self, algorithmName, algo: AlgorithmDefinition):
        self.algorithmName = algorithmName
        
        super().__init__(algo.data)

        # Strategy: MACD crossover
        # macd        : EMA(Shorter Period) - EMA(Longer Period)
        # macd_signal : EMA(MACD, 9 days)
        # macd_diff   : macd - macd_signal
        self.data["macd"] = round_result(MACD(close=self.data["Close"]).macd())
        self.data["macd_signal"] = round_result(MACD(close=self.data["Close"]).macd_signal())
        self.data["macd_diff"] = round_result(MACD(close=self.data["Close"]).macd_diff())

        # Algo: Generate trading signals
        self.data['BuyCondition'] = self.data["macd_diff"] > 0
        self.data['SellCondition'] = self.data["macd_diff"] < 0
