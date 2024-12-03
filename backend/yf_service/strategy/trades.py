import pandas as pd

class Trades:
    def __init__(self, strategy: pd.DataFrame):
        """
        Class that is responsible for the determination of buy and sell trades.
        """
        self._data = strategy._df.copy()
        
        # signal determination
        self._data["BuySignal"] = self.determine_signals(data=self._data["BuyCondition"])
        self._data["BuyPrice"] = self.determine_price_at_signal(data=self._data, signal='BuySignal')
        
        # price determination
        self._data["SellSignal"] = self.determine_signals(data=self._data["SellCondition"])
        self._data["SellPrice"] = self.determine_price_at_signal(data=self._data, signal='SellSignal')

    @staticmethod
    def determine_signals(data):
        """
        Given a pandas Series of boolean values, return a new Series where only the first occurrence
        of True and the first occurrence of False are retained, and all other values are set to None.
        """
        found_true = False
        result = []

        for value in data:
            if value and not found_true:
                result.append(True)
                found_true = True
            elif not value:
                result.append(None)
                found_true = False  # reset flag when a False is encountered
            else:
                result.append(None)

        return pd.Series(result, index=data.index)
    
    @staticmethod
    def determine_price_at_signal(data, signal):
        """
        Returns the price when the price signal is True, otherwise None.
        """
        return data["Close"].where(data[signal].notna(), None)
