from db_service.db import DB_Client
from models.result_model import ResultsModel
from models.strategy_model import StrategyModel
from setup_logging.setup_logging import logger
from yf_service.common.core import get_yf_stock_data
from yf_service.strategy.results import Results
from yf_service.strategy.trades import Trades
from yf_service.strategy.handler import StrategyHandler

class StrategyDB_Client(DB_Client):
    def __init__(self):
        super().__init__()

    def get_trades_for_code(self, code: str) -> dict:
        try:
            logger.info("get_trades_for_code: Getting all trades")
            strategy = self.session.query(StrategyModel).filter_by(code=code).order_by(StrategyModel.date).all()

            if strategy:
                logger.info(f"get_trades_for_code: Trades were fetched for {code}.")
                response_data = {
                    'code': code,
                    'results': [
                        {
                            'country': trade.country,
                            'date': trade.date.strftime('%Y-%m-%d'),
                            'close_price': trade.close_price,
                            'buy_signal': trade.buy_signal,
                            'buy_price': trade.buy_price,
                            'sell_signal': trade.sell_signal,
                            'sell_price': trade.sell_price,
                        } for trade in strategy
                    ]
                }
                return response_data
            
            else:
                logger.info(f"get_trades_for_code: No trades fetched for {code}.")
                return None
            
        except Exception as e:
            self.session.rollback()
            logger.error(f"get_trades_for_code error: {e}")
            raise Exception(f"Failed to add strategy data: {e}")

    def get_results_for_code(self, code: str):
        try:
            logger.info("get_results_for_code: Getting all results")
            result = self.session.query(ResultsModel).filter_by(code=code).first()

            if result:
                logger.info(f"get_results_for_code: Results were fetched for {code}.")
                response_data = {
                    'code': result.code,
                    'country': result.country,
                    'initial_investment': result.initial_investment,
                    'buy_sell_pairs_timestamp': result.buy_sell_pairs_timestamp,
                    'profit_loss_shares': result.profit_loss_shares,
                    'strategy_roi': result.strategy_roi,
                    'total_profit': result.total_profit,
                    'total_profit_per_trade': result.total_profit_per_trade,
                    'total_number_of_trades': result.total_number_of_trades,
                    'number_profit_trades': result.number_profit_trades,
                    'number_loss_trades': result.number_loss_trades,
                    'pct_win': result.pct_win,
                    'pct_loss': result.pct_loss,
                    'greatest_profit': result.greatest_profit,
                    'greatest_loss': result.greatest_loss,
                }
                return response_data
            
            else:
                logger.info(f"get_results_for_code: No results fetched for {code}.")
                return None

        except Exception as e:
            self.session.rollback()
            logger.error(f"get_results_for_code error: {e}")
            raise Exception(f"Failed to get strategy results: {e}")

    def add_strategy_for_code(self, json_data: dict) -> bool:
        try:
            logger.info("add_strategy_for_code: Adding individual strategy")
            code = json_data.get('code')
            country = json_data.get('country')
            strategy_name = json_data.get('strategy')
            time_period = json_data.get('time_period')
            time_interval = json_data.get('time_interval')
            window_slow = json_data.get('window_slow')
            window_fast = json_data.get('window_fast')
            logger.info(f"Received: {code} | {country} | {strategy_name} | {time_period} | {time_interval} | {window_slow} | {window_fast} ")

            logger.info("Checking for existing strategy and results.")
            existing_strategy = self.session.query(StrategyModel).filter_by(code=code).first()
            existing_results = self.session.query(ResultsModel).filter_by(code=code).first()

            if existing_strategy or existing_results:
                logger.info("Strategy or results found.")
                return False

            if not code or not country or not strategy_name or not time_period or not time_interval or not window_slow or not window_fast:
                logger.info("Missing required fields: 'code', 'country', 'strategy_name', 'time_period', 'time_interval', 'window_slow' or 'window_fast'.")
                raise ValueError("Missing required fields: 'code', 'country', 'strategy_name', 'time_period', 'time_interval', 'window_slow' or 'window_fast'.")

            if isinstance(window_slow, str):
                window_slow = int(window_slow)

            if isinstance(window_fast, str):
                window_fast = int(window_fast)

            logger.info("Retrieving stock data.")
            df = get_yf_stock_data(
                ticker=code, 
                time_period=time_period, 
                time_interval=time_interval
            )

            logger.info("Determining strategy")
            handler = StrategyHandler(data=df)
            strategy = handler.get_strategy(
                strategy_name=strategy_name,
                window_slow=window_slow,
                window_fast=window_fast
            )

            logger.info("Checking for strategy existence")
            trades = Trades(strategy)
            existing_strategy = self.session.query(StrategyModel).filter_by(code=code).first()
            logger.info(f"Output from quering StrategyModel to check if strategy already exists: {existing_strategy}")
            
            if not existing_strategy:
                logger.info(f"Adding strategy for {code} to db.")
                for index, row in trades._data.iterrows():
                    cl = float(row['Close'].iloc[0])
                    bs = row['BuySignal'].iloc[0]
                    bp = row['BuyPrice'].iloc[0]
                    ss = row['SellSignal'].iloc[0]
                    sp = row['SellPrice'].iloc[0]

                    new_strategy_entry = StrategyModel(
                        code=code,
                        country=country,
                        date=index.date(),
                        close_price=cl,
                        buy_signal=bs,
                        buy_price=bp,
                        sell_signal=ss,
                        sell_price=sp
                    )
                    self.session.add(new_strategy_entry)
                logger.info(f"Added strategy for {code} to db.")

            logger.info("Checking for results existence")
            results = Results(trades)
            existing_results = self.session.query(ResultsModel).filter_by(code=code).first()
            logger.info(f"Output from quering ResultsModel to check if strategy already exists: {existing_results}")
            
            if not existing_results:
                logger.info(f"Adding results for {code} to db.")
                new_result_entry = ResultsModel(
                    code=code,
                    country=country,
                    initial_investment = results.INITIAL_INVESTMENT,
                    buy_sell_pairs_timestamp = results.buy_sell_pairs_timestamp,
                    profit_loss_shares = results.profit_loss_shares,
                    strategy_roi = results.strategy_roi,
                    total_profit=results.total_profit,
                    total_profit_per_trade=results.total_profit_per_trade,
                    total_number_of_trades=results.total_number_of_trades,
                    number_profit_trades=results.number_profit_trades,
                    number_loss_trades=results.number_loss_trades,
                    pct_win=results.pct_win,
                    pct_loss=results.pct_loss,
                    greatest_profit=results.greatest_profit,
                    greatest_loss=results.greatest_loss
                )
                self.session.add(new_result_entry)
                logger.info(f"Added results for {code} to db.")
            
            self.session.commit()
            return True
            
        except ValueError as ve:
            self.session.rollback()
            logger.error(f"add_strategy_for_code ValueError: {ve}")
            raise ve
        
        except Exception as e:
            self.session.rollback()
            logger.error(f"add_strategy_for_code error: {e}")
            raise Exception(f"Failed to add strategy data: {e}")
        
    def delete_strategy_for_code(self, code: str):
        try:
            logger.info("delete_strategy_for_code: Deleting strategy and result")
            strategy = self.session.query(StrategyModel).filter_by(code=code).first()
            result = self.session.query(ResultsModel).filter_by(code=code).first()

            if not strategy or not result:
                logger.info(f"Strategy or result not found for {code}")
                return False
            
            if strategy:
                logger.info(f"Strategy found. Deleting for stock {code}.")
                self.session.delete(strategy)

            if result:
                logger.info(f"Results found. Deleting for stock {code}.")
                self.session.delete(result)

            self.session.commit()

            logger.info(f"Finished deleting strategy or results for stock {code}.")
            return True

        except Exception as e:
            self.session.rollback()
            logger.error(f"delete_strategy_for_code error: {e}")
            raise Exception(f"Failed to delete strategy data: {e}")
        
strategyDB_Client = StrategyDB_Client()