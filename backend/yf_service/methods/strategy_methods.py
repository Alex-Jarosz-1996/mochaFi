from db_service.db import DB_Client
from models.result_model import ResultsModel
from models.strategy_model import StrategyModel
from yf_service.common.core import get_yf_stock_data
from yf_service.strategy.results import Results
from yf_service.strategy.trades import Trades
from yf_service.strategy.handler import StrategyHandler

class StrategyDB_Client(DB_Client):
    def __init__(self):
        super().__init__()

    def get_trades_for_code(self, code: str) -> dict:
        try:
            strategy = self.session.query(StrategyModel).filter_by(code=code).order_by(StrategyModel.date).all()

            if strategy:
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
                return None
            
        except Exception as e:
            self.session.rollback()
            raise Exception(f"Failed to add strategy data: {e}")

    def get_results_for_code(self, code: str):
        try:
            result = self.session.query(ResultsModel).filter_by(code=code).first()

            if result:
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
                return None

        except Exception as e:
            self.session.rollback()
            raise Exception(f"Failed to get strategy results: {e}")

    def add_strategy_for_code(self, json_data: dict) -> bool:
        try:
            code = json_data.get('code')
            country = json_data.get('country')
            strategy_name = json_data.get('strategy')
            time_period = json_data.get('time_period')
            time_interval = json_data.get('time_interval')
            window_slow = json_data.get('window_slow')
            window_fast = json_data.get('window_fast')

            existing_strategy = self.session.query(StrategyModel).filter_by(code=code).first()
            existing_results = self.session.query(ResultsModel).filter_by(code=code).first()

            if existing_strategy or existing_results:
                return False

            if not code or not country or not strategy_name or not time_period or not time_interval or not window_slow or not window_fast:
                raise ValueError("Missing required fields: 'code', 'country', 'strategy_name', 'time_period', 'time_interval', 'window_slow' or 'window_fast'.")

            if isinstance(window_slow, str):
                window_slow = int(window_slow)

            if isinstance(window_fast, str):
                window_fast = int(window_fast)

            df = get_yf_stock_data(
                ticker=code, 
                time_period=time_period, 
                time_interval=time_interval
            )

            handler = StrategyHandler(data=df)
            strategy = handler.get_strategy(
                strategy_name=strategy_name,
                window_slow=window_slow,
                window_fast=window_fast
            )

            trades = Trades(strategy)
            existing_strategy = self.session.query(StrategyModel).filter_by(code=code).first()
            if not existing_strategy:
                for index, row in trades._data.iterrows():
                    new_strategy_entry = StrategyModel(
                        code=code,
                        country=country,
                        date=index.date(),
                        close_price=row['Close'],
                        buy_signal=row['BuySignal'],
                        buy_price=row['BuyPrice'],
                        sell_signal=row['SellSignal'],
                        sell_price=row['SellPrice']
                    )
                    self.session.add(new_strategy_entry)

            results = Results(trades)
            existing_results = self.session.query(ResultsModel).filter_by(code=code).first()
            if not existing_results:
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
            
            self.session.commit()
            return True
            
        except ValueError as ve:
            self.session.rollback()
            raise ve
        
        except Exception as e:
            self.session.rollback()
            raise Exception(f"Failed to add strategy data: {e}")
        
    def delete_strategy_for_code(self, code: str):
        try:
            strategy = self.session.query(StrategyModel).filter_by(code=code).first()
            result = self.session.query(ResultsModel).filter_by(code=code).first()

            if not strategy or not result:
                return False
            
            if strategy:
                self.session.delete(strategy)

            if result:
                self.session.delete(result)

            self.session.commit()

            return True

        except Exception as e:
            self.session.rollback()
            raise Exception(f"Failed to delete strategy data: {e}")
        
strategyDB_Client = StrategyDB_Client()