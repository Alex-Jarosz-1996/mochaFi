from core.algo_core import AlgorithmDefinition
from ta.momentum import RSIIndicator


class Strategy(AlgorithmDefinition):
    def __init__(
        self, algorithmName, algo: AlgorithmDefinition, slow_window=14, fast_window=2
    ):
        self.algorithmName = algorithmName

        super().__init__(algo.data)

        # Strategy: RSI crossover
        self.data["rsi_slow"] = RSIIndicator(
            close=self.data["Close"], window=slow_window
        ).rsi()
        self.data["rsi_fast"] = RSIIndicator(
            close=self.data["Close"], window=fast_window
        ).rsi()

        # Algo: Generate trading signals
        self.data["BuyCondition"] = self.data["rsi_fast"] > self.data["rsi_slow"]
        self.data["SellCondition"] = self.data["rsi_fast"] < self.data["rsi_slow"]
