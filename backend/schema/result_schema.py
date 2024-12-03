from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from models.result_model import ResultsModel

class ResultsSchema(SQLAlchemySchema):
    class Meta:
        model = ResultsModel
        load_instance = True  # Enables deserialization into model instances

    id = auto_field()
    code = auto_field()
    country = auto_field()
    initial_investment = auto_field()
    buy_sell_pairs_timestamp = auto_field()
    profit_loss_shares = auto_field()
    strategy_roi = auto_field()
    total_profit = auto_field()
    total_profit_per_trade = auto_field()
    total_number_of_trades = auto_field()
    number_profit_trades = auto_field()
    number_loss_trades = auto_field()
    pct_win = auto_field()
    pct_loss = auto_field()
    greatest_profit = auto_field()
    greatest_loss = auto_field()

results_schema = ResultsSchema(many=True)