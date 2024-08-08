import requests
import pandas as pd
from bs4 import BeautifulSoup

def getYahooFinanceStockURL(stockTicker):
    """
    Returns information about stock from Yahoo Finance website
    """
    return f'https://au.finance.yahoo.com/quote/{stockTicker}.AX/key-statistics?p={stockTicker}.AX'

def getMarketWatchStockURL(stockTicker):
    """
    Returns information about stock from Market Watch website
    """

    return f'https://www.marketwatch.com/investing/stock/{stockTicker}?countrycode=au&mod=over_search'

def yahooFinanceData(stockTicker):
    """
    Returns all stock data as soup from Yahoo Finance Website
    """
    
    try:
        stockURL = getYahooFinanceStockURL(stockTicker)
    except Exception as e:
        print(f'error in yahooFinanceData(): {stockTicker}')
        print(e)
        return None
    else:
        r = requests.get(stockURL, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'})
        return pd.read_html(r.text)

def marketWatchData(stockTicker):
    """
    Returns all stock data as soup from Market Watch Website
    """
    
    try:
        stockURL = getMarketWatchStockURL(stockTicker)
    except Exception as e:
        print(f'error in yahooFinanceData(): {stockTicker}')
        print(e)
        return None
    else:
        requestsPage = requests.get(stockURL)
        return BeautifulSoup(requestsPage.content, 'html.parser')

