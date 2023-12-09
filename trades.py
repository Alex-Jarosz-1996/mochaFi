import pandas as pd

class BuySellTrades:
    def __init__(self, strategy_obj):
        self.data = strategy_obj.data

        # Determining transition of signals (ie (False, True, True) -> (False, True, False)):
        self.data['BuySignal'] = self.determine_signal(self.data["BuyCondition"])
        self.data['SellSignal'] = self.determine_signal(self.data["SellCondition"])

        # Determining Buy and Sell Price of True Signal:
        self.data['BuyPrice'] = self.determine_price_at_signal(self.data['BuySignal'], self.data["Close"])
        self.data['SellPrice'] = self.determine_price_at_signal(self.data['SellSignal'], self.data["Close"])

    @staticmethod
    def determine_signal(lst):
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

        
