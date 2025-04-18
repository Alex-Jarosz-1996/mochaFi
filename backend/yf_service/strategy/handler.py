import pandas as pd
from yf_service.strategy.ma import Strategy_MA
from yf_service.strategy.macd import Strategy_MACD
from yf_service.strategy.rsi import Strategy_RSI
from yf_service.strategy.vw_macd import Strategy_VW_MACD

class StrategyHandler:
    def __init__(self, data: pd.DataFrame):
        """
        Initialize the handler with the data.
        """
        self.data = data

        # Mapping strategy names to their respective classes
        self.strategy_map = {
            "MA": Strategy_MA,
            "MACD": Strategy_MACD,
            "RSI": Strategy_RSI,
            "VW_MACD": Strategy_VW_MACD
        }

    def get_strategy(self, strategy_name: str, **kwargs):
        """
        Returns the requested strategy instance.
        """
        strategy_class = self.strategy_map.get(strategy_name)

        if not strategy_class:
            raise ValueError(f"Strategy '{strategy_name}' is not supported.")

        # Return an instance of the strategy, passing the data and any additional parameters
        return strategy_class(self.data, **kwargs)
