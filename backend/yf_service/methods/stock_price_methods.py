from db_service.db import DB_Client
from models.stock_price_model import StockPriceModel
from setup_logging.setup_logging import logger
from yf_service.common.core import get_yf_stock_data

class StockPriceDB_Client(DB_Client):
    def __init__(self):
        super().__init__()

    def get_stock_price(self, code: str) -> dict:
        """
        Fetches all stock prices for a given stock code.
        """
        try:
            logger.info("get_stock_price: Getting all stock prices")
            prices = (
                self.session.query(StockPriceModel)
                .filter_by(code=code)
                .order_by(StockPriceModel.date)
                .all()
            )

            if not prices:
                logger.info(f"get_stock_price: No stock prices were fetched for {code}.")
                return None

            logger.info(f"get_stock_price: Stock prices were fetched for {code}.")
            return {
                "code": code,
                "prices": [
                    {
                        "date": price.date.strftime('%Y-%m-%d'),
                        "open": price.open_price,
                        "high": price.high_price,
                        "low": price.low_price,
                        "close": price.close_price,
                        "volume": price.volume,
                    }
                    for price in prices
                ],
            }

        except Exception as e:
            self.session.rollback()
            logger.error(f"get_stock_price error: {e}")
            raise Exception(f"Failed to fetch stock prices for code {code}: {e}")

    
    def add_individual_stock_price(self, json_data: dict) -> bool:
        """
        Adds individual stock price data to the database for a given stock code.
        """
        try:
            logger.info("add_individual_stock_price: Adding individual stock price")
            code = json_data.get("code")
            country = json_data.get("country")
            time_period = json_data.get("time_period")
            time_interval = json_data.get("time_interval")
            logger.info(f"Received: {code} | {country} | {time_period} | {time_interval}")

            logger.info("Checking for existing stock price")
            existing_stock_price = self.session.query(StockPriceModel).filter_by(code=code).first()
            if existing_stock_price:
                logger.info(f"Stock prices found for {code}")
                return False

            logger.info("Parsing json structure to ensure that all fields are present.")
            if not code or not country or not time_period or not time_interval:
                logger.error("Missing required fields: 'code', 'country', 'time_period', or 'time_interval'.")
                raise ValueError("Missing required fields: 'code', 'country', 'time_period', or 'time_interval'.")

            logger.info("Retrieving stock prices.")
            df = get_yf_stock_data(ticker=code, time_period=time_period, time_interval=time_interval)
            logger.info(f"Output from get_yf_stock_data: {df}")

            logger.info("Checking that output df contains all columns names.")
            required_fields = ['Open', 'High', 'Low', 'Close', 'Volume']
            for required_field in required_fields:
                if required_field not in df.columns:
                    logger.error(f"{required_field} not present in {df.columns}")
                    raise ValueError(f"Missing required columns in data: {', '.join(required_field)}")

            logger.info("Checking that all columns in output df are of consistent length")
            if not all(len(df[col]) == df.shape[0] for col in df.columns):
                logger.error("All columns in the data must have the same length.")
                raise ValueError("All columns in the data must have the same length.")

            existing_stock_price = self.session.query(StockPriceModel).filter_by(code=code).first()
            logger.info(f"Output from quering StockPriceModel to check if code already exists: {existing_stock_price}")

            if not existing_stock_price:
                logger.info(f"Adding stock prices for {code} to db.")
                for index, row in df.iterrows():
                    new_price = StockPriceModel(
                        code=code,
                        country=country,
                        date=index.date(),
                        open_price=row['Open'],
                        high_price=row['High'],
                        low_price=row['Low'],
                        close_price=row['Close'],
                        volume=float(row['Volume'])
                    )
                    self.session.add(new_price)
                logger.info(f"Added stock prices for {code} to db.")

            self.session.commit()
            return True

        except ValueError as ve:
            self.session.rollback()
            logger.error(f"add_individual_stock_price ValueError: {ve}")
            raise ve

        except Exception as e:
            self.session.rollback()
            logger.error(f"add_individual_stock_price error: {e}")
            raise Exception(f"Failed to add stock price data: {e}")


    def delete_all_stock_price(self) -> int:
        """
        Deletes all stock price data from the database.
        """
        try:
            logger.info("delete_all_stock_price: Deleting all stock prices")
            rows_deleted = self.session.query(StockPriceModel).delete()
            self.session.commit()

            logger.info(f"Deleted {rows_deleted} rows.")
            return rows_deleted

        except Exception as e:
            self.session.rollback()
            logger.error(f"delete_all_stock_price error: {e}")
            raise Exception(f"Failed to delete all stock price data: {e}")
        
stockPriceDB_Client = StockPriceDB_Client()