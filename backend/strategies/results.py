import pandas as pd

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
        self._data = strategy._data.copy()
        self.buy_sell_pairs = self.determine_buy_sell_pairs()
        self.total_profit = self.determine_total_profit()
        self.total_profit_per_trade = self.determine_total_profit_per_trade()
        self.total_number_of_trades = self.determine_number_of_trades()
        self.number_profit_trades = self.determine_number_profit_trades()
        self.number_loss_trades = self.determine_number_loss_trades()
        self.pct_win = self.determine_pct_win_from_strategy()
        self.pct_loss = self.determine_pct_loss_from_strategy()
        self.greatest_profit = self.determine_greatest_profit()
        self.greatest_loss = self.determine_greatest_loss()

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

    def determine_total_profit(self):
        """
        Calculates the total profit or loss from all buy/sell pairs.
        """
        total = 0
        for result in self.buy_sell_pairs:
            buy_price = result[0]
            sell_price = result[-1]
            total += (sell_price - buy_price)
        
        return total

    def determine_total_profit_per_trade(self):
        """
        Calculates the profit or loss for each buy/sell pair.
        """
        profit = []
        for result in self.buy_sell_pairs:
            buy_price = result[0]
            sell_price = result[-1]
            profit.append(sell_price - buy_price)
        
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
        return pct_win

    def determine_pct_loss_from_strategy(self):
        """
        Calculates the percentage of trades that resulted in a loss.
        """
        num_loss = self.number_loss_trades
        total_num_trades = self.total_number_of_trades
        pct_loss = num_loss / total_num_trades
        return pct_loss

    def determine_greatest_profit(self):
        """
        Identifies the highest profit from a single trade.
        """
        return max(self.total_profit_per_trade)

    def determine_greatest_loss(self):
        """
        Identifies the largest loss from a single trade.
        """
        return min(self.total_profit_per_trade)