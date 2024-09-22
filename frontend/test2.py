import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def getYahooFinanceStockURL(stockTicker):
    """
    Returns information about stock from Yahoo Finance website
    """
    return f"https://au.finance.yahoo.com/quote/{stockTicker}.AX/"
    # return f"https://au.finance.yahoo.com/quote/{stockTicker}.AX/key-statistics?p={stockTicker}.AX"

if __name__ == "__main__":
    stock = "CBA"
    url = getYahooFinanceStockURL(stock)

    # response = requests.get(url)
    response = requests.get(
        url=url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        },
    )
    html_content = response.text
    
    soup = bs(html_content, 'html.parser')

    element = soup.find('fin-streamer', {'data-test': 'qsp-price'})
    
    if element:
        # Get the price from the 'value' attribute
        price = element['value']
        print(f"The current price is: {price} | {type(price)}")
        
        # Alternatively, get the price from the text content
        # price = element.text
        # print(f"The current price is: {price}")
    else:
        print("Element not found")


