import yfinance as yf
import pandas as pd

from setup_logging.setup_logging import logger


def get_yf_stock_data(
    ticker: str, 
    time_period: str = "1y", 
    time_interval: str = "1d"
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
        logger.info("Download data")
        data = yf.download(tickers=ticker, period=time_period, interval=time_interval)
        
        logger.info("Convert to pandas DataFrame")
        df = pd.DataFrame(data)

        logger.info("Round specified columns to 2 decimal places")
        columns_to_round = ['Open', 'High', 'Low', 'Close']
        df[columns_to_round] = df[columns_to_round].round(2)
        
        return df

    except Exception as e:
        logger.error(f"get_yf_stock_data error: {e}")
        return None


def round_result(result):
    """
    Rounds result to 2 dp.
    """
    return round(result, 2)
