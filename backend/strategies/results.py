import math
import pandas as pd

from backend.common.core import round_result

class Results:
    """
    Class that provides the following information about each strategy:
    1. Number of Buy / Sell Pairs
    2. Total Profit / Loss from Buy / Sell Pairs
    3. Profit / Loss from each Buy / Sell Pairs
    4. Number of profitable / loss trades
    5. Pct win / loss
    6. Greatest profit / loss
    """
    
    def __init__(self, strategy: pd.DataFrame):
        """
        Initializes the Results object with strategy data.
        """
        self.INITIAL_INVESTMENT = 1000
        
        self._data = strategy._data.copy()
        self.buy_sell_pairs_timestamp = self.collect_buy_sell_pairs_datetime()
        self.buy_sell_pairs = self.determine_buy_sell_pairs()
        self.profit_loss_shares = self.determine_profit_loss_dependent_on_shares()
        self.strategy_roi = self.determine_strategy_roi()
        self.total_profit = self.determine_total_profit()
        self.total_profit_per_trade = self.determine_total_profit_per_trade()
        self.total_number_of_trades = self.determine_number_of_trades()
        self.number_profit_trades = self.determine_number_profit_trades()
        self.number_loss_trades = self.determine_number_loss_trades()
        self.pct_win = self.determine_pct_win_from_strategy()
        self.pct_loss = self.determine_pct_loss_from_strategy()
        self.greatest_profit = self.determine_greatest_profit()
        self.greatest_loss = self.determine_greatest_loss()

    
    def collect_buy_sell_pairs_datetime(self):
        """
        Collects date-time buy/sell pairs with their respective datetime timestamp.
        Ex:
        [
            (yyyy-mm-dd, buy_price1, yyyy-mm-dd, sell_price1),
            (yyyy-mm-dd, buy_price2, yyyy-mm-dd, sell_price2),
            ...
            (yyyy-mm-dd, buy_priceN, yyyy-mm-dd, sell_priceN)
        ]
        """
        buy_sell_pairs = []
        current_buy = None
        
        for index, row in self._data.iterrows():
            date = index.date().strftime('%Y-%m-%d') # aid serialisation from json to str
            close_price = row['Close']
            buy_signal = row['BuySignal']
            sell_signal = row['SellSignal']
            
            # Check for a buy signal
            if buy_signal == True:
                current_buy = (date, close_price)
            
            # Check for a sell signal if there's a recorded buy
            if sell_signal == True and current_buy:
                buy_date, buy_price = current_buy
                sell_date = date
                sell_price = close_price
                buy_sell_pairs.append((buy_date, buy_price, sell_date, sell_price))
                current_buy = None
        
        return buy_sell_pairs
    
    
    def determine_buy_sell_pairs(self):
        """
        Identifies and returns a list of buy/sell pairs from the strategy data.
        """
        buy_prices = self._data['BuyPrice']
        sell_prices = self._data['SellPrice']

        pairs = []
        current_buy = None

        for buy_price, sell_price in zip(buy_prices, sell_prices):
            if current_buy is None and not pd.isna(buy_price):
                current_buy = buy_price

            elif current_buy is not None and not pd.isna(sell_price):
                pairs.append((current_buy, sell_price))
                current_buy = None

        return pairs

    
    def determine_profit_loss_dependent_on_shares(self):
        """
        Determine profit / loss per trade multiplied by number of shares.
        Returns profit per trade and sell date.
        """
        buy_sell_pairs = self.collect_buy_sell_pairs_datetime()
        
        profit_per_trade_list = []
        for buy_sell_pair in buy_sell_pairs:
            buy_price, sell_date, sell_price = buy_sell_pair[1], buy_sell_pair[2], buy_sell_pair[-1]

            num_shares = math.floor(self.INITIAL_INVESTMENT / buy_price)
            profit_per_trade = round(num_shares * (sell_price - buy_price), 2)

            profit_per_trade_list.append((sell_date, profit_per_trade))
            
        return profit_per_trade_list
    

    def determine_strategy_roi(self):
        """
        Determines strategy Return on Investment for investment period as a pct of initial investment.
        """
        total_profit = 0
        for profit in self.determine_profit_loss_dependent_on_shares():
            total_profit += profit[-1]

        strategy_roi = 100 * (total_profit / self.INITIAL_INVESTMENT)
        return strategy_roi
    
    
    def determine_total_profit(self):
        """
        Calculates the total profit or loss from all buy/sell pairs.
        """
        total = 0
        for result in self.buy_sell_pairs:
            buy_price = result[0]
            sell_price = result[-1]
            total += (sell_price - buy_price)
        
        return round_result(total)

    def determine_total_profit_per_trade(self):
        """
        Calculates the profit or loss for each buy/sell pair.
        """
        profit = []
        for result in self.buy_sell_pairs:
            buy_price = result[0]
            sell_price = result[-1]
            profit.append(round_result(sell_price - buy_price))
        
        return profit

    def determine_number_of_trades(self):
        """
        Determines the total number of buy/sell pairs (trades).
        """
        return len(self.buy_sell_pairs)

    def determine_number_profit_trades(self):
        """
        Calculates the number of trades that resulted in a profit.
        """
        num_profit = 0
        for result in self.buy_sell_pairs:
            buy_price = result[0]
            sell_price = result[-1]
            if sell_price > buy_price:
                num_profit += 1
        
        return num_profit

    def determine_number_loss_trades(self):
        """
        Calculates the number of trades that resulted in a loss.
        """
        num_loss = 0
        for result in self.buy_sell_pairs:
            buy_price = result[0]
            sell_price = result[-1]
            if sell_price < buy_price:
                num_loss += 1
        
        return num_loss

    def determine_pct_win_from_strategy(self):
        """
        Calculates the percentage of trades that resulted in a profit.
        """
        num_profit = self.number_profit_trades
        total_num_trades = self.total_number_of_trades
        pct_win = num_profit / total_num_trades
        return round_result(pct_win * 100)

    def determine_pct_loss_from_strategy(self):
        """
        Calculates the percentage of trades that resulted in a loss.
        """
        num_loss = self.number_loss_trades
        total_num_trades = self.total_number_of_trades
        pct_loss = num_loss / total_num_trades
        return round_result(pct_loss * 100)

    def determine_greatest_profit(self):
        """
        Identifies the highest profit from a single trade.
        """
        return round_result(max(self.total_profit_per_trade))

    def determine_greatest_loss(self):
        """
        Identifies the largest loss from a single trade.
        """
        return round_result(min(self.total_profit_per_trade))
