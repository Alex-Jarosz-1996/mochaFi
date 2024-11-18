import re
import requests
import asyncio
import websockets
import json
import datetime
import os

from dotenv import load_dotenv

from typing import List

from websocket_tastyworks_client import WebSocketTastyWorksClient

load_dotenv()

class TastyWorksClient:
    def __init__(self):
        self.base_url = os.getenv('TASTYWORKS_BASE_URL')
        self.account_number = os.getenv('TASTYWORKS_ACCOUNT_NUMBER')
        self.login = os.getenv('TASTYWORKS_LOGIN')
        self.password = os.getenv('TASTYWORKS_PASSWORD')
        self.remember_me = True

        self._session_token = self.generate_session_token()
    
    def _build_headers(self, include_auth: bool = False) -> dict:
        """
        Constructs the standard headers for the requests.
        """
        headers = {
            "User-Agent": "tastytrade-api-client/1.0",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        if include_auth and self._session_token:
            headers["Authorization"] = self._session_token
        return headers
    
    def generate_session_token(self) -> str:
        """
        Creates an active session.

        API endpoint; POST: /sessions
        """
        try:
            data = {
                "login": self.login,
                "password": self.password,
                "remember-me": self.remember_me
            }

            response = requests.post(f"{self.base_url}/sessions", 
                                    headers=self._build_headers(), 
                                    json=data, 
                                    timeout=10)

            response.raise_for_status()
            
            return response.json()['data']['session-token']

        except requests.exceptions.HTTPError as e:
            print(f"Error: {e}")
            raise requests.exceptions.HTTPError
        
        
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None
    
    
    def get_api_quote_token(self) -> dict:
        """
        Retrieves api quote tokens, required for streaming
        market data.

        API endpoint; GET: /api-quote-tokens
        """
        try:
            response = requests.get(f"{self.base_url}/api-quote-tokens",
                                    headers=self._build_headers(include_auth=True),
                                    timeout=10)
            
            response.raise_for_status()
            
            return response.json()
        
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None


    def is_account_active(self) -> bool:
        """
        Retrieves customer account details.

        API endpoint; GET: /customers/me/accounts/{account_number}
        """
        try:
            response = requests.get(f"{self.base_url}/customers/me/accounts/{self.account_number}",
                                    headers=self._build_headers(include_auth=True),
                                    timeout=10)
            
            response.raise_for_status()

            response_obj = response.json()
            is_closed = response_obj.get('data', None).get('is-closed', None)
            return True if is_closed == False else False
        
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None
        

    def is_options_trading_allowed(self):
        """
        Determines whether options trading is allowed on account.

        API endpoint; GET: /accounts/{account_number}/trading-status
        """
        try:
            response = requests.get(f"{self.base_url}/accounts/{self.account_number}/trading-status",
                                    headers=self._build_headers(include_auth=True),
                                    timeout=10)
            
            response.raise_for_status()

            response_obj = response.json()
            options_trading_allowed = response_obj.get('data', None).get('options-level', None)

            return True if options_trading_allowed == 'No Restrictions' else False

        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None
        
    
    def get_current_active_positions(self):
        """
        Determines current open positions

        API endpoint; GET: /accounts/{account_number}/positions
        """
        try:
            response = requests.get(f"{self.base_url}/accounts/{self.account_number}/positions",
                                    headers=self._build_headers(include_auth=True),
                                    timeout=10)
            
            response.raise_for_status()

            response_obj = response.json()

            open_positions = response_obj.get('data', None).get('items', None)

            return None if len(open_positions) == 0 else open_positions

        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None
        
    
    def get_current_account_balance(self):
        """
        Get current account balance.

        API endpoint; GET: /accounts/{account_number}/balances
        """
        try:
            response = requests.get(f"{self.base_url}/accounts/{self.account_number}/balances",
                                    headers=self._build_headers(include_auth=True),
                                    timeout=10)
            
            response.raise_for_status()

            response_obj = response.json()

            current_cash_balance = response_obj.get('data', None).get('cash-balance', None)

            return current_cash_balance

        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None


    @staticmethod
    def clean_option_information(option: str):
        """
        Removes ticker and whitespace before option.
        >>> clean_option_information("AAPL  241213P00300000")
        ' 241213P00300000 '
        """
        result = re.sub(r'^[A-Za-z]+\s+', '', option)
        return result
    
    @staticmethod
    def format_option_contract(contract):
        # Extract year, month, day, call/put, and strike price parts
        year = contract[:2]
        month = contract[2:4]
        day = contract[4:6]
        option_type = 'Call' if contract[6] == 'C' else 'Put'
        strike_price = int(contract[7:]) / 1000  # Strike price needs to be divided by 1000
        
        # Convert year, month, and day into the desired date format
        date_obj = datetime.datetime.strptime(f"{year}{month}{day}", "%y%m%d")
        formatted_date = date_obj.strftime("%b %d %y")  # Format to 'Nov 08 24'
        
        # Construct the final formatted string
        formatted_contract = f"{formatted_date}, {int(strike_price)} {option_type}"
        return formatted_contract
    
    
    def get_ticker_options_chain(self, ticker: str):
        """
        Gets option chain for ticker, if option chain exists.

        API endpoint; GET: /option-chains/{ticker}/compact
        """
        try:
            response = requests.get(f"{self.base_url}/option-chains/{ticker}/compact",
                                    headers=self._build_headers(include_auth=True),
                                    timeout=10)
            
            response.raise_for_status()

            response_obj = response.json()

            contracts_list = []
            contracts_iterator = response_obj.get('data', None).get('items', None)
            for i in range(len(contracts_iterator)):
                contracts = contracts_iterator[i].get('symbols', None)
                for contract in contracts:
                    contracts_list.append(contract)

            option_list = []
            for option in contracts_list:
                cleaned_option = self.clean_option_information(option)
                option_list.append(self.format_option_contract(cleaned_option))

            return option_list

        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None
        

    def get_ticker_options_chain_tradeable(self, ticker: str):
        """
        Gets option chain for ticker, in a trade-able form that is
        recogniseable by tastytrade, if option chain exists.

        API endpoint; GET: /option-chains/{ticker}/compact
        """
        try:
            response = requests.get(f"{self.base_url}/option-chains/{ticker}/compact",
                                    headers=self._build_headers(include_auth=True),
                                    timeout=10)
            
            response.raise_for_status()

            response_obj = response.json()

            contracts_list = []
            contracts_iterator = response_obj.get('data', None).get('items', None)
            for i in range(len(contracts_iterator)):
                contracts = contracts_iterator[i].get('streamer-symbols', None)
                for contract in contracts:
                    contracts_list.append(contract)

            return contracts_list

        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None
        
    
    def get_all_tradeable_cryptocurrencies(self):
        """
        Gets all tradeable cryptocurrencies, available to tastytrade.

        API endpoint; GET: /instruments/cryptocurrencies/
        """
        try:
            response = requests.get(f"{self.base_url}/instruments/cryptocurrencies/",
                                    headers=self._build_headers(include_auth=True),
                                    timeout=10)
            
            response.raise_for_status()

            response_obj = response.json()

            all_cryptos_data = response_obj.get('data', None).get('items', None)

            print(all_cryptos_data)
            
            cryptos_list = []
            for i in range(len(all_cryptos_data)):
                crypto = all_cryptos_data[i].get('symbol', None)
                cryptos_list.append(crypto.replace('/USD', '')) # removing USD as currency

            return cryptos_list

        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None
