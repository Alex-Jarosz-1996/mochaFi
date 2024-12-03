from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Date,
    UniqueConstraint,
)
from models.base import Base

class StrategyModel(Base):
    __tablename__ = "trades"

    id = Column(Integer, primary_key=True)
    code = Column(String(8), nullable=True)
    country = Column(String(5), nullable=True)
    date = Column(Date, nullable=True)
    close_price = Column(Float, nullable=True)
    buy_signal = Column(Float, nullable=True)
    buy_price = Column(Float, nullable=True)
    sell_signal = Column(Float, nullable=True)
    sell_price = Column(Float, nullable=True)

    __table_args__ = (UniqueConstraint('code', 'date', name='uix_trades_date'),)
