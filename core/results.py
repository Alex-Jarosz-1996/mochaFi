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


