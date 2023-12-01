from ta.trend import MACD
import yfinance as yf

from core import *

# Fetch historical data
# formatted_date = datetime.today().date().strftime('%Y-%m-%d')
# data = yf.download('AAPL', start='2020-01-01', end=formatted_date)
data = yf.download('SPY', period="5y", interval="1d")
data = data.drop("Adj Close", axis=1).round(2)

# Strategy: MACD crossover
# macd        : EMA(Shorter Period) - EMA(Longer Period)
# macd_signal : EMA(MACD, 9 days)
# macd_diff   : macd - macd_signal
data["macd"] = round_result(MACD(close=data["Close"]).macd())
data["macd_signal"] = round_result(MACD(close=data["Close"]).macd_signal())
data["macd_diff"] = round_result(MACD(close=data["Close"]).macd_diff())

# Algo: Generate trading signals
data['BuyCondition'] = data["macd_diff"] > 0
data['SellCondition'] = data["macd_diff"] < 0

# Determining transition of signals (ie (False, True, True) -> (False, True, False)):
data['BuySignal'] = determine_signal(data["BuyCondition"])
data['SellSignal'] = determine_signal(data["SellCondition"])

# Determining Buy and Sell Price of True Signal:
data['BuyPrice'] = determine_price_at_signal(data['BuySignal'], data["Close"])
data['SellPrice'] = determine_price_at_signal(data['SellSignal'], data["Close"])

# Grouping Buy and Sell Signals:
buy_sell_pairs = map_buy_sell_actions(data['BuyPrice'], data['SellPrice'])
print(f"Buy/Sell pairs: {buy_sell_pairs}")

# Determining number or buy, sell pairs
num_buy_sell_pairs = get_num_buy_sell_pairs(buy_sell_pairs)
print(f"Number Buy/Sell pairs: {num_buy_sell_pairs}")

# Determining profit:
profit_per_trade = profit_calculator_per_instance(buy_sell_pairs)
print(f"Profit per trade: {profit_per_trade}")

num_profit_trades = number_profit_trades(profit_per_trade)
print(f"Number of profitable trades: {num_profit_trades}")

num_loss_trades = number_loss_trades(profit_per_trade)
print(f"Number of loss trades: {num_loss_trades}")

pct_win, pct_loss = pct_win_loss_trades(profit_per_trade)
print(f"% trades won: {round_result(pct_win*100)}%")
print(f"% trades loss: {round_result(pct_loss*100)}%")

gp = greatest_profit(profit_per_trade)
print(f"Greatest profit: ${gp}")

gl = greatest_loss(profit_per_trade)
print(f"Greatest loss: ${gl}")

total_profit = profit_calculator(profit_per_trade)
print(f"Total profit: ${round_result(total_profit)}")