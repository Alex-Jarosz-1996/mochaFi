import pandas as pd

from algo_core import AlgorithmDefinition
from core import get_yf_stock_data, round_result
from results import StrategyResult
from trades import BuySellTrades

# from MA_50_200_day import Strategy
# from MACD_crossover import Strategy
from MACD_crossover_inverted import Strategy 


     
if __name__ == "__main__":
    data = get_yf_stock_data("SPY", "5y")
    
    algo_defs = AlgorithmDefinition(data)
    
    strategy = Strategy("MACD_crossover", algo_defs)
    
    trades = BuySellTrades(strategy)
    
    results = StrategyResult(trades)

