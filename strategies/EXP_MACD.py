from ta.trend import ema_indicator

from core.algo_core import AlgorithmDefinition
from core.yf_core import round_result

class Strategy(AlgorithmDefinition):
    def __init__(self, algorithmName, algo: AlgorithmDefinition):
        self.algorithmName = algorithmName
        
        super().__init__(algo.data)

        # Strategy: MACD crossover
        # macd        : EMA(Shorter Period) - EMA(Longer Period)
        # macd_signal : EMA(MACD, 9 days)
        # macd_diff   : macd - macd_signal
        short_period = 12
        long_period = 26
        signal_period = 9

        # Calculate MACD
        self.data["macd"] = round_result(self.calculate_ema(self.data["Close"], short_period) -
                                         self.calculate_ema(self.data["Close"], long_period))

        # Calculate MACD Signal
        self.data["macd_signal"] = round_result(self.calculate_ema(self.data["macd"], signal_period))

        # Calculate MACD Diff
        self.data["macd_diff"] = round_result(self.data["macd"] - self.data["macd_signal"])

        # Algo: Generate trading signals
        self.data['BuyCondition'] = self.data["macd_diff"] > 0
        self.data['SellCondition'] = self.data["macd_diff"] < 0

    @staticmethod
    def calculate_ema(series, span):
        return ema_indicator(series, span)
