import pandas as pd

class Trades:
    def __init__(self, strategy: pd.DataFrame):
        """
        Class that is responsible for the determination of buy and sell trades.
        """
        self._data = strategy._df.copy()
        
        # signal determination
        self._data["BuySignal"] = self.determine_signals(condition="BuyCondition")
        self._data["SellSignal"] = self.determine_signals(condition="SellCondition")
        
        # price determination
        self._data["BuyPrice"] = self.determine_price_at_signal(signal="BuySignal")
        self._data["SellPrice"] = self.determine_price_at_signal(signal="SellSignal")

    def determine_signals(self, condition):
        """
        Given a pandas Series of boolean values, return a new Series where only the first occurrence
        of True and the first occurrence of False are retained, and all other values are set to None.
        """
        found_true = False
        result = []

        for value in self._data[condition]:
            if value and not found_true:
                result.append(True)
                found_true = True
            elif not value:
                result.append(False)
                found_true = False  # reset flag when a False is encountered
            else:
                result.append(False)

        return pd.Series(result, index=self._data[condition].index)
    
    def determine_price_at_signal(self, signal):
        """
        Returns the price when the price signal is True, otherwise None.
        """
        return self._data["Close"].where(self._data[signal] == True, False)
