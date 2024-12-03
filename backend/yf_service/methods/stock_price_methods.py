from db_service.db import DB_Client
from models.stock_price_model import StockPriceModel
from yf_service.common.core import get_yf_stock_data

class StockPriceDB_Client(DB_Client):
    def __init__(self):
        super().__init__()

    def get_stock_price(self, code: str) -> dict:
        """
        Fetches all stock prices for a given stock code.
        """
        try:
            prices = (
                self.session.query(StockPriceModel)
                .filter_by(code=code)
                .order_by(StockPriceModel.date)
                .all()
            )

            if not prices:
                return None

            return {
                "code": code,
                "prices": [
                    {
                        "date": price.date.strftime('%Y-%m-%d'),
                        "open": price.open_price,
                        "high": price.high_price,
                        "low": price.low_price,
                        "close": price.close_price,
                        "adj_close": price.adj_close_price,
                        "volume": price.volume,
                    }
                    for price in prices
                ],
            }

        except Exception as e:
            self.session.rollback()
            raise Exception(f"Failed to fetch stock prices for code {code}: {e}")

    
    def add_individual_stock_price(self, json_data: dict) -> bool:
        """
        Adds individual stock price data to the database for a given stock code.
        """
        try:
            code = json_data.get("code")
            country = json_data.get("country")
            time_period = json_data.get("time_period")
            time_interval = json_data.get("time_interval")

            existing_stock_price = self.session.query(StockPriceModel).filter_by(code=code).first()
            if existing_stock_price:
                return False

            if not code or not country or not time_period or not time_interval:
                raise ValueError("Missing required fields: 'code', 'country', 'time_period', or 'time_interval'.")

            df = get_yf_stock_data(ticker=code, time_period=time_period, time_interval=time_interval)

            required_fields = ['Open', 'High', 'Low', 'Close', 'Adj_Close', 'Volume']
            for required_field in required_fields:
                if required_field not in df.columns:
                    raise ValueError(f"Missing required columns in data: {', '.join(required_field)}")

            if not all(len(df[col]) == df.shape[0] for col in df.columns):
                raise ValueError("All columns in the data must have the same length.")

            existing_stock_price = self.session.query(StockPriceModel).filter_by(code=code).first()

            if not existing_stock_price:
                for index, row in df.iterrows():
                    new_price = StockPriceModel(
                        code=code,
                        country=country,
                        date=index.date(),
                        open_price=row['Open'],
                        high_price=row['High'],
                        low_price=row['Low'],
                        close_price=row['Close'],
                        adj_close_price=row['Adj_Close'],
                        volume=row['Volume']
                    )
                    self.session.add(new_price)

            self.session.commit()
            return True

        except ValueError as ve:
            self.session.rollback()
            raise ve

        except Exception as e:
            self.session.rollback()
            raise Exception(f"Failed to add stock price data: {e}")


    def delete_all_stock_price(self) -> int:
        """
        Deletes all stock price data from the database.
        """
        try:
            rows_deleted = self.session.query(StockPriceModel).delete()
            self.session.commit()

            return rows_deleted

        except Exception as e:
            self.session.rollback()
            raise Exception(f"Failed to delete all stock price data: {e}")
        
stockPriceDB_Client = StockPriceDB_Client()