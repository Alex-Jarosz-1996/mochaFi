import pandas as pd

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