from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Date,
    BigInteger,
    UniqueConstraint,
)
from models.base import Base

class StockPriceModel(Base):
    __tablename__ = "stock_price_history"

    id = Column(Integer, primary_key=True)
    code = Column(String(8), nullable=True)
    country = Column(String(5), nullable=True)
    date = Column(Date, nullable=True)
    open_price = Column(Float, nullable=True)
    high_price = Column(Float, nullable=True)
    low_price = Column(Float, nullable=True)
    close_price = Column(Float, nullable=True)
    volume = Column(BigInteger, nullable=True)

    # Composite unique constraint to ensure no duplicate entries for a stock on a given date
    __table_args__ = (UniqueConstraint('code', 'date', name='uix_stock_date'),)