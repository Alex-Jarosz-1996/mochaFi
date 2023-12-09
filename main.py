import pandas as pd

from core import get_yf_stock_data, round_result

class AlgorithmDefinition:
    def __init__(self, algorithmName, stock_data):
        self.algorithmName = algorithmName
        self.data = stock_data


class Strategy(AlgorithmDefinition):
    def __init__(self, algo: AlgorithmDefinition):
        super().__init__(algo.algorithmName, algo.data)
        
        # Strategy: Calculate moving averages
        self.data['MA50'] = round(algo.data['Close'].rolling(50).mean(), 2)
        self.data['MA200'] = round(algo.data['Close'].rolling(200).mean(), 2)

        # Algo: Generate trading signals
        self.data['BuyCondition'] = (self.data['MA50'] > self.data['MA200'])
        self.data['SellCondition'] = (self.data['MA200'] > self.data['MA50'])


class BuySellTrades:
    def __init__(self, strategy_obj: Strategy):
        self.data = strategy_obj.data

        # Determining transition of signals (ie (False, True, True) -> (False, True, False)):
        self.data['BuySignal'] = self.determine_signal(self.data["BuyCondition"])
        self.data['SellSignal'] = self.determine_signal(self.data["SellCondition"])

        # Determining Buy and Sell Price of True Signal:
        self.data['BuyPrice'] = self.determine_price_at_signal(self.data['BuySignal'], self.data["Close"])
        self.data['SellPrice'] = self.determine_price_at_signal(self.data['SellSignal'], self.data["Close"])

    @staticmethod
    def determine_signal(lst: pd.Series):
        result = []
        consecutive = False  # Flag to track if the current True values are consecutive

        for value in lst:
            if value:
                if not consecutive:
                    # The first True, keep it as is
                    result.append(True)
                    consecutive = True
                else:
                    # Consecutive True values, set to False
                    result.append(False)
            else:
                # False value, keep it as is
                result.append(False)
                consecutive = False

        return result


    @staticmethod
    def determine_price_at_signal(bool_series, float_series):
        result = []
        
        # Make sure the two series have the same index
        if not bool_series.index.equals(float_series.index):
            raise ValueError("The input Series must have the same index.")
        
        # Iterate through the series
        for index, bool_value in bool_series.items():
            if bool_value:
                result.append(float_series[index])
            else:
                result.append(0)
        
        # Create a new Series with the preserved index
        result_series = pd.Series(result, index=bool_series.index)
        
        return result_series

        
        
class StrategyResult:
    def __init__(self, buy_sell_trades_obj):
        self.data = buy_sell_trades_obj.data
        self.buy_sell_pairs = self.map_buy_sell_actions(self.data['BuyPrice'], self.data['SellPrice'])
        self.num_buy_sell_pairs = self.get_num_buy_sell_pairs(self.buy_sell_pairs)
        self.profit_per_trade = self.profit_calculator_per_instance(self.buy_sell_pairs)
        self.num_profit_trades, self.num_loss_trades = self.calculate_profit_loss_trades(self.profit_per_trade)
        self.pct_win, self.pct_loss = self.calculate_pct_win_loss(self.profit_per_trade)
        self.greatest_profit = max(self.profit_per_trade)
        self.greatest_loss = min(self.profit_per_trade)
        self.total_profit = sum(self.profit_per_trade)

    
    @staticmethod
    def map_buy_sell_actions(buy_prices, sell_prices):
        actions = []
        current_buy_price = 0

        for buy_price, sell_price in zip(buy_prices, sell_prices):
            if buy_price != 0:
                current_buy_price = buy_price
            elif sell_price != 0 and current_buy_price != 0:
                actions.append((current_buy_price, sell_price))
                current_buy_price = 0

        return actions

    @staticmethod
    def get_num_buy_sell_pairs(lst):
        return len(lst)

    @staticmethod
    def profit_calculator_per_instance(tuple_list):
        return [round(val2 - val1, 2) for val1, val2 in tuple_list]

    @staticmethod
    def calculate_profit_loss_trades(lst):
        num_profit = sum(1 for i in lst if i > 0)
        num_loss = sum(1 for i in lst if i <= 0)
        return num_profit, num_loss

    @staticmethod
    def calculate_pct_win_loss(lst):
        total_trades = len(lst)
        num_profit = sum(1 for i in lst if i > 0)
        num_loss = total_trades - num_profit
        pct_win = (num_profit / total_trades) * 100 if total_trades > 0 else 0
        pct_loss = (num_loss / total_trades) * 100 if total_trades > 0 else 0
        return pct_win, pct_loss



if __name__ == "__main__":
    data = get_yf_stock_data("SPY", "5y")
    
    algo_defs = AlgorithmDefinition("MA_50_200_day", data)
    
    strategy = Strategy(algo_defs)
    
    trades = BuySellTrades(strategy)
    
    results = StrategyResult(trades)

