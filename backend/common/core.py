import yfinance as yf
import pandas as pd


def get_yf_stock_data(
    ticker: str, time_period: str = "1y", time_interval: str = "1d"
) -> pd.DataFrame:
    """
    Retrieve stock data using Yahoo Finance API.

    NOTE:
    >>> ticker        : "stock1" or "stock1 stock2 stockn"
    >>> time_period   : 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
    >>> time_interval : 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
    """

    if not isinstance(ticker, str):
        return None

    try:
        # Download data
        data = yf.download(tickers=ticker, period=time_period, interval=time_interval)
        
        # Convert to pandas DataFrame
        df = pd.DataFrame(data)

        # Renaming Column name to not cause error
        df.rename(columns={'Adj Close': 'Adj_Close'}, inplace=True)

        # Round specified columns to 2 decimal places
        columns_to_round = ['Open', 'High', 'Low', 'Close', 'Adj_Close']
        df[columns_to_round] = df[columns_to_round].round(2)
        
        return df

    except Exception as e:
        print(f"Error occured: {e}")
        return None


def round_result(result):
    """
    Rounds result to 2 dp.
    """
    return round(result, 2)
