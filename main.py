from core.algo_core import AlgorithmDefinition
from core.yf_core import get_yf_stock_data
from core.results import StrategyResult
from core.trades import BuySellTrades

from strategies.VW_MACD import Strategy

     
if __name__ == "__main__":
    data = get_yf_stock_data("SPY", "5y")
    
    algo_defs = AlgorithmDefinition(data)
    
    strategy = Strategy("MACD_crossover", algo_defs)
    
    trades = BuySellTrades(strategy)
    
    results = StrategyResult(trades)
    print(results.total_profit)
