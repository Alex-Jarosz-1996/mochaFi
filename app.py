import os

from backend.common.core import get_yf_stock_data
from backend.data.utils.controller import StockController
from flask import Flask, request, jsonify

# from backend import get_yf_stock_data
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

# initialising flask app
app = Flask(__name__)

# Configuring db
db_path = os.path.join(os.path.dirname(__file__), 'app.db')
db_uri = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db = SQLAlchemy(app)

CORS(app=app)

class Stock(db.Model):
    __tablename__ = "stock"
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(8), unique=True, nullable=False)
    country = db.Column(db.String(5))

    def __init__(self, code, country):
        self.code = code
        self.country = country


class FinancialData(db.Model):
    __tablename__ = 'financial_data'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.Integer, db.ForeignKey('stock.code'), nullable=False)
    price = db.Column(db.Float)
    volume = db.Column(db.Integer)
    eps = db.Column(db.Float)
    pe_ratio = db.Column(db.Float)


# TODO: ADD
# class StockChart(db.Model):
#     __tablename__ = "stock_chart"


# TODO: ADD
# class BackTest(db.Model):
#     __tablename__ = "back_test"


# TODO: ADD
# class TradeBot(db.Model):
#     __tablename__ = "trade_bot"

@app.route('/stats', methods=['GET', 'POST'])
def get_stock_data():
    if request.method == 'GET':
        pass

    if request.method == 'POST':
        data = request.json
        country = data.get('country')
        code    = data.get('code')

        if not country or not code:
            return jsonify({"error": "Missing 'stock_type' or 'ticker' parameter"}), 400
        
        try:
            # determining which object to use
            obj = StockController(code, country)
            
            # saving to database
            stock = Stock(code=obj.si.ticker, 
                            country=obj.si.country)
            db.session.add(stock)
            db.session.commit()

            response = {
                "code": stock.code,
                "country": stock.country
            }
            return jsonify(response), 200
        
        except Exception as e:
            return jsonify({"error": str(e)}), 400



@app.route('/chart', methods=['GET', 'POST'])
def chart():
    if request.method == 'GET':
        ticker = request.args.get('ticker', default=None)
        time_period = request.args.get('time_period', default=None)
        time_interval = request.args.get('time_interval', default='1d')

        if ticker is None or time_period is None:
            return jsonify({"error": "Missing parameters"}), 400

        data = get_yf_stock_data(ticker, time_period, time_interval)

        if data is not None:
            return jsonify(data.to_dict(orient='split'))
        else:
            return jsonify({"error": "Data retrieval failed"}), 500

    elif request.method == 'POST':
        data = request.get_json()
        ticker = data.get('ticker', None)
        time_period = data.get('time_period', None)
        time_interval = data.get('time_interval', '1d')

        if ticker is None or time_period is None:
            return jsonify({"error": "Missing parameters"}), 400

        data = get_yf_stock_data(ticker, time_period, time_interval)

        if data is not None:
            return jsonify(data.to_dict(orient='split'))
        else:
            return jsonify({"error": "Data retrieval failed"}), 500

if __name__ == '__main__':
    app.run(debug=True)
