from ta.momentum import RSIIndicator

from core.algo_core import AlgorithmDefinition
from core.yf_core import round_result

class Strategy(AlgorithmDefinition):
    def __init__(self, algorithmName, algo: AlgorithmDefinition):
        self.algorithmName = algorithmName
        
        super().__init__(algo.data)

        # Strategy: RSI crossover
        self.data["rsi_14day"] = RSIIndicator(close=self.data["Close"], window=14).rsi()
        self.data["rsi_2day"] = RSIIndicator(close=self.data["Close"], window=2).rsi()

        # Algo: Generate trading signals
        self.data['BuyCondition'] = self.data["rsi_2day"] > self.data["rsi_14day"]
        self.data['SellCondition'] = self.data["rsi_2day"] < self.data["rsi_14day"]
