from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    JSON,
)
from models.base import Base

class ResultsModel(Base):
    __tablename__ = "results"

    id = Column(Integer, primary_key=True)
    code = Column(String(8), unique=True, nullable=True)
    country = Column(String(5), nullable=True)
    initial_investment = Column(Float, nullable=True)
    buy_sell_pairs_timestamp = Column(JSON, nullable=True)
    profit_loss_shares = Column(JSON, nullable=True)
    strategy_roi = Column(Float, nullable=True)
    total_profit = Column(Float, nullable=True)
    total_profit_per_trade = Column(JSON, nullable=True)
    total_number_of_trades = Column(Integer, nullable=True)
    number_profit_trades = Column(Integer, nullable=True)
    number_loss_trades = Column(Integer, nullable=True)
    pct_win = Column(Float, nullable=True)
    pct_loss = Column(Float, nullable=True)
    greatest_profit = Column(Float, nullable=True)
    greatest_loss = Column(Float, nullable=True)
