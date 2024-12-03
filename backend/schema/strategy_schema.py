from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from models.strategy_model import StrategyModel

class StrategySchema(SQLAlchemySchema):
    class Meta:
        model = StrategyModel
        load_instance = True  # Enables deserialization into model instances

    id = auto_field()
    code = auto_field()
    country = auto_field()
    date = auto_field()
    close_price = auto_field()
    buy_signal = auto_field()
    buy_price = auto_field()
    sell_signal = auto_field()
    sell_price = auto_field()

strategy_schema = StrategySchema(many=True)