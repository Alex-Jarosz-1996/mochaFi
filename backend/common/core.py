import yfinance as yf
from pandas import DataFrame


def get_yf_stock_data(
    ticker: str, time_period: str, time_interval: str = "1d"
) -> DataFrame:
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
        data = yf.download(tickers=ticker, period=time_period, interval=time_interval)
        data = data.drop("Adj Close", axis=1).round(2)
        return data

    except Exception as e:
        print(f"Error occured: {e}")
        return None


def round_result(result):
    num_dp = 2
    return round(result, num_dp)
