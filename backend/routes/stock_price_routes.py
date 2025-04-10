from http import HTTPStatus
from flask import Blueprint, jsonify, request

from setup_logging.setup_logging import logger

from yf_service.methods.stock_price_methods import stockPriceDB_Client


stock_price_bp = Blueprint("stock_price", __name__)


@stock_price_bp.route("/<string:code>", methods=["GET"])
def get_stock_prices(code):
    """
    API endpoint to get all stock price data for a stock from the database.
    """
    try:
        logger.info("Executing GET /api/stock_price/<string:code> endpoint.")
        result = stockPriceDB_Client.get_stock_price(code)
        logger.info(f"Received GET /api/stock_price/<string:code> with output: {result}")

        if result is not None:
            logger.info("Stock prices found. Returning HTTP 200 Ok status.")
            return jsonify(result), HTTPStatus.OK

        logger.info(f"No prices found for stock code {code}")
        return jsonify({"error": f"No prices found for stock code {code}"}), HTTPStatus.NOT_FOUND

    except Exception as e:
        logger.error(f"Type Error: {type(str(e))}. Error: {str(e)}")
        return jsonify({"error": "Unexpected error occurred", "details": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


@stock_price_bp.route("/", methods=["POST"])
def add_stock_prices():
    """
    API endpoint to add stock price data for a given stock code.
    """
    try:
        logger.info("Executing POST /api/stock_price endpoint.")
        data = request.get_json()
        logger.info(f"Received POST /api/stock_price with output: {data}")

        if not data:
            logger.error("Error: Invalid or missing JSON data.")
            return jsonify({"error": "Invalid or missing JSON data"}), HTTPStatus.BAD_REQUEST

        result = stockPriceDB_Client.add_individual_stock_price(data)
        logger.info(f"Result from stockPriceDB_Client.add_individual_stock_price: {result}")

        if result:
            logger.info(f"Added stock price structure for code {data.get('code')}")
            return jsonify({"message": f"Added stock price structure for code {data.get('code')}"}), HTTPStatus.CREATED
        
        else:
            logger.info(f"Stock price structure already exists for code {data.get('code')}.")
            return jsonify({"error": f"Stock price structure already exists for code {data.get('code')}."}), HTTPStatus.CONFLICT

    except ValueError as ve:
        logger.error(f"Type Error: ValueError. Error: {str(ve)}")
        return jsonify({"error": str(ve)}), HTTPStatus.BAD_REQUEST

    except Exception as e:
        logger.error(f"Type Error: {type(str(e))}. Error: {str(e)}")
        return jsonify({"error": "Unexpected error occurred", "details": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


@stock_price_bp.route("/", methods=["DELETE"])
def delete_all_stock_price_histories():
    """
    API endpoint to delete all stock price information saved within the database.
    """
    try:
        logger.info("Executing DELETE /api/stock_price endpoint.")
        rows_deleted = stockPriceDB_Client.delete_all_stock_price()
        logger.info(f"Received DELETE /api/stock_price with output: {rows_deleted}")

        if rows_deleted > 0:
            logger.info("Deleted all stock price histories successfully")
            return jsonify({"message": "Deleted all stock price histories successfully"}), HTTPStatus.OK

        logger.info("No stock price histories deleted")
        return jsonify({"message": "No stock price histories deleted"}), HTTPStatus.NOT_FOUND
    
    except Exception as e:
        logger.error(f"Type Error: {type(str(e))}. Error: {str(e)}")
        return jsonify({"error": "Unexpected error occurred", "details": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
