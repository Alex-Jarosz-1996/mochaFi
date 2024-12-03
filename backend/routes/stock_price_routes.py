from http import HTTPStatus
from flask import Blueprint, jsonify, request

from yf_service.methods.stock_price_methods import stockPriceDB_Client


stock_price_bp = Blueprint("stock_price", __name__)


@stock_price_bp.route("/<string:code>", methods=["GET"])
def get_stock_prices(code):
    """
    API endpoint to get all stock price data for a stock from the database.
    """
    try:
        result = stockPriceDB_Client.get_stock_price(code)

        if result is not None:
            return jsonify(result), HTTPStatus.OK

        return jsonify({"error": f"No prices found for stock code {code}"}), HTTPStatus.NOT_FOUND

    except Exception as e:
        return jsonify({"error": "Unexpected error occurred", "details": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


@stock_price_bp.route("/", methods=["POST"])
def add_stock_prices():
    """
    API endpoint to add stock price data for a given stock code.
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "Invalid or missing JSON data"}), HTTPStatus.BAD_REQUEST

        result = stockPriceDB_Client.add_individual_stock_price(data)

        if result:
            return jsonify({"message": f"Added stock price structure for code {data.get('code')}"}), HTTPStatus.CREATED
        
        else:
            return jsonify({"error": f"Stock price structure already exists for code {data.get('code')}."}), HTTPStatus.CONFLICT

    except ValueError as ve:
        return jsonify({"error": str(ve)}), HTTPStatus.BAD_REQUEST

    except Exception as e:
        return jsonify({"error": "Unexpected error occurred", "details": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


@stock_price_bp.route("/", methods=["DELETE"])
def delete_all_stock_price_histories():
    """
    API endpoint to delete all stock price information saved within the database.
    """
    try:
        rows_deleted = stockPriceDB_Client.delete_all_stock_price()

        if rows_deleted > 0:
            return jsonify({"message": "Deleted all stock price histories successfully"}), HTTPStatus.OK

        return jsonify({"message": "No stock price histories deleted"}), HTTPStatus.NOT_FOUND
    
    except Exception as e:
        return jsonify({"error": "Unexpected error occurred", "details": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
