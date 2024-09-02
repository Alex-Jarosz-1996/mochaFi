import os

from flask import Flask, jsonify, request

# from backend import get_yf_stock_data
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from backend.common.core import get_yf_stock_data
from backend.data.utils.controller import StockController

# initialising flask app
app = Flask(__name__)
CORS(app=app)

# Configuring db
db_path = os.path.join(os.path.dirname(__file__), "app.db")
db_uri = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class StockModel(db.Model):
    __tablename__ = "stock"
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(8), unique=True, nullable=False)
    country = db.Column(db.String(5), unique=False, nullable=False)

    def __repr__(self):
        return f"<Stock {self.stock}>"


# TODO: ADD
# class FinancialData(db.Model):
#     __tablename__ = 'financial_data'
#     id = db.Column(db.Integer, primary_key=True)
#     code = db.Column(db.Integer, db.ForeignKey('stock.code'), nullable=False)


# TODO: ADD
# class StockChart(db.Model):
#     __tablename__ = "stock_chart"


# TODO: ADD
# class BackTest(db.Model):
#     __tablename__ = "back_test"


# TODO: ADD
# class TradeBot(db.Model):
#     __tablename__ = "trade_bot"


# Create the database tables
with app.app_context():
    db.create_all()

# API route to handle stock selection and save to database
@app.route('/stock', methods=['POST'])
def add_stock():
    data = request.json
    code = data.get('stock')
    country = data.get('country')

    print(f"Received request to add stock: {code} from {country}")

    # Check if the stock-country combination already exists
    existing_stock = StockModel.query.filter_by(code=code, country=country).first()
    if existing_stock:
        return jsonify({"error": "Stock already exists"}), 409

    stock_obj = StockController(code, country)
    
    new_stock = StockModel(code=stock_obj.si.ticker, country=stock_obj.si.country)
    db.session.add(new_stock)
    db.session.commit()

    return jsonify({
        "message": "Stock added successfully",
        "code": code,
        "country": country
    }), 201


@app.route('/stocks', methods=['GET'])
def get_stocks():
    stocks = StockModel.query.all()
    return jsonify([
        {"id": stock.id, "code": stock.code, "country": stock.country}  # Changed 'stock' to 'code'
        for stock in stocks
    ])


@app.route('/stock/<int:stock_id>', methods=['DELETE'])
def delete_stock(stock_id):
    try:
        stock = StockModel.query.get(stock_id)
        if not stock:
            return jsonify({"error": "Stock not found"}), 404

        db.session.delete(stock)
        db.session.commit()

        return jsonify({"message": "Stock deleted successfully"}), 200
    except Exception as e:
        print(f"Error deleting stock: {e}")
        return jsonify({"error": "Error deleting stock"}), 500


if __name__ == "__main__":
    app.run(debug=True)