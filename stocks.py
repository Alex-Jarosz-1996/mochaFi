import pandas as pd
import yfinance as yf
from datetime import datetime

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


def map_buy_sell_actions(buy_prices, sell_prices):
    actions = []

    # Create a DataFrame with BuyPrice and SellPrice columns
    df = pd.DataFrame({'BuyPrice': buy_prices, 'SellPrice': sell_prices})

    # Initialize a variable to track the current BuyPrice
    current_buy_price = 0

    # Iterate through the DataFrame
    for _, row in df.iterrows():
        # If it's a BuyPrice, update the current_buy_price
        if row['BuyPrice'] != 0:
            current_buy_price = row['BuyPrice']
        # If it's a SellPrice, add the pair to the actions list
        elif row['SellPrice'] != 0 and current_buy_price != 0:
            actions.append((current_buy_price, row['SellPrice']))
            current_buy_price = 0  # Reset current_buy_price

    return actions


def profit_calculator_per_instance(tuple_list):
    return_list = []
    
    for i in tuple_list:
        val1, val2 = i
        vals_difference = round(val2 - val1, 2)
        return_list.append(vals_difference)

    return return_list


def profit_calculator(lst):
    return_value = 0

    for i in lst:
        return_value += i

    return return_value


def get_num_buy_sell_pairs(lst):
    return len(lst)


def number_profit_trades(lst):
    num_profit = 0
    for i in lst:
        if i > 0:
            num_profit += 1

    return num_profit


def number_loss_trades(lst):
    num_loss = 0
    for i in lst:
        if i <= 0:
            num_loss += 1

    return num_loss


def pct_win_loss_trades(lst):
    num_profit = 0
    num_loss = 0
    
    for i in lst:
        if i > 0:
            num_profit += 1
        else:
            num_loss += 1

    pct_won = num_profit / len(lst)
    pct_lost = num_loss / len(lst)

    return pct_won, pct_lost


def greatest_profit(lst):
    return max(lst)


def greatest_loss(lst):
    return min(lst)


# Fetch historical data
# formatted_date = datetime.today().date().strftime('%Y-%m-%d')
# data = yf.download('AAPL', start='2020-01-01', end=formatted_date)
data = yf.download('AAPL', period="5y", interval="1d")
data = data.drop("Adj Close", axis=1).round(2)

# Strategy: Calculate moving averages
data['MA50'] = round(data['Close'].rolling(50).mean(), 2)
data['MA200'] = round(data['Close'].rolling(200).mean(), 2)

# Algo: Generate trading signals
data['BuyCondition'] = (data['MA50'] > data['MA200'])
data['SellCondition'] = (data['MA200'] > data['MA50'])

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
print(f"% trades won: {round(pct_win*100)}%")
print(f"% trades loss: {round(pct_loss*100)}%")

gp = greatest_profit(profit_per_trade)
print(f"Greatest profit: ${gp}")

gl = greatest_loss(profit_per_trade)
print(f"Greatest loss: ${gl}")

# total_profit = profit_calculator(profit_per_trade)
# print(f"Total profit: {total_profit}")

