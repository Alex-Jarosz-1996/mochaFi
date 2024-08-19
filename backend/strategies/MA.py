from core.algo_core import AlgorithmDefinition


class Strategy(AlgorithmDefinition):
    def __init__(
        self, algorithmName, algo: AlgorithmDefinition, slow_window=200, fast_window=50
    ):
        self.algorithmName = algorithmName

        super().__init__(algo.data)

        # Strategy: Calculate moving averages
        self.data["MA_fast"] = round(algo.data["Close"].rolling(fast_window).mean(), 2)
        self.data["MA_slow"] = round(algo.data["Close"].rolling(slow_window).mean(), 2)

        # Algo: Generate trading signals
        self.data["BuyCondition"] = self.data["MA_fast"] > self.data["MA_slow"]
        self.data["SellCondition"] = self.data["MA_slow"] > self.data["MA_fast"]
