from flask import Blueprint

from routes.stock_routes import stock_bp
from routes.stock_price_routes import stock_price_bp
from routes.strategy_routes import strategy_bp

def register_routes(app):
    app.register_blueprint(stock_bp, url_prefix="/api/stock")
    app.register_blueprint(stock_price_bp, url_prefix="/api/stock_price")
    app.register_blueprint(strategy_bp, url_prefix="/api/strategy")
