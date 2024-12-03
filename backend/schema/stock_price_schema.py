from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from models.stock_price_model import StockPriceModel

class StockPriceSchema(SQLAlchemySchema):
    class Meta:
        model = StockPriceModel
        load_instance = True  # Allows deserialization to model instances

    id = auto_field()
    code = auto_field()
    country = auto_field()
    date = auto_field()
    open_price = auto_field()
    high_price = auto_field()
    low_price = auto_field()
    close_price = auto_field()
    adj_close_price = auto_field()
    volume = auto_field()

stock_price_schema = StockPriceSchema(many=True)