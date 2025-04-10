from http import HTTPStatus
from flask import Blueprint, jsonify, request

from sqlalchemy.exc import IntegrityError

from schema.stock_schema import StockSchema
from setup_logging.setup_logging import logger
from yf_service.methods.stock_methods import stockDB_Client


stock_bp = Blueprint("stock", __name__)


@stock_bp.route("/", methods=["GET"])
def get_stocks():
    """
    API endpoint to get all stocks from the database.
    """
    try:
        logger.info("Executing GET /api/stock endpoint.")
        result = stockDB_Client.get_all_stocks()
        logger.info(f"Received GET /api/stock with output: {result}")
        
        if result is not None:
            logger.info("Stocks found. Returning HTTP 200 Ok status.")
            if isinstance(result, list):
                return jsonify(StockSchema(many=True).dump(result)), HTTPStatus.OK
            else:
                return jsonify(StockSchema().dump(result)), HTTPStatus.OK
        
        logger.info("No stocks found")
        return jsonify({"error": "No stocks found"}), HTTPStatus.NOT_FOUND
    
    except Exception as e:
        logger.error(f"Type Error: {type(str(e))}. Error: {str(e)}")
        return jsonify({"error": "Failed to fetch stocks", "details": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


@stock_bp.route("/", methods=["POST"])
def add_stock():
    """
    API endpoint to add a single stock to the database.
    """
    try:
        logger.info("Executing POST /api/stock endpoint.")
        data = request.get_json()
        logger.info(f"Received POST /api/stock with output: {data}")
        
        if not data:
            logger.error("Error: Invalid or missing JSON data.")
            return jsonify({"error": "Invalid or missing JSON data"}), HTTPStatus.BAD_REQUEST

        result = stockDB_Client.add_single_stock(json_data=data)
        logger.info(f"Result from stockDB_Client.add_single_stock: {result}")

        if result:
            logger.info(f"Stock {data.get('code')} successfully")
            return jsonify({"message": f"Stock {data.get('code')} successfully"}), HTTPStatus.OK
    
    except ValueError as ve:
        logger.error(f"Type Error: ValueError. Error: {str(ve)}")
        return jsonify({"error": str(ve)}), HTTPStatus.CONFLICT

    except TypeError as te:
        logger.error(f"Type Error: TypeError. Error: {str(te)}")
        return jsonify({"error": str(te)}), HTTPStatus.INTERNAL_SERVER_ERROR

    except IntegrityError:
        logger.error(f"Type Error: IntegrityError. Stock {data.get('code')} already added")
        return jsonify({"error": f"Stock {data.get('code')} already added."}), HTTPStatus.INTERNAL_SERVER_ERROR
    
    except Exception as e:
        logger.error(f"Type Error: {type(str(e))}. Error: {str(e)}")
        return jsonify({"error": "Unexpected error occurred", "details": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


@stock_bp.route("/", methods=["DELETE"])
def delete_all_stocks():
    """
    API endpoint to remove all stocks from the database.
    """
    try:
        logger.info("Executing DELETE /api/stock endpoint.")
        result = stockDB_Client.delete_all_stocks()
        logger.info(f"Received DELETE /api/stock with output: {result}")

        if result:
            logger.info("All stocks deleted successfully")
            return jsonify({"message": "All stocks deleted successfully"}), HTTPStatus.OK

        logger.info("No stocks to delete")
        return jsonify({"message": "No stocks to delete"}), HTTPStatus.NOT_FOUND

    except Exception as e:
        logger.error(f"Type Error: {type(str(e))}. Error: {str(e)}")
        return jsonify({"error": "Unexpected error occurred", "details": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


@stock_bp.route("/<int:stock_id>", methods=["DELETE"])
def delete_stock(stock_id):
    """
    API endpoint to remove single stock from the database.
    """
    try:
        logger.info("Executing DELETE /api/stock/<int:stock_id> endpoint.")
        result = stockDB_Client.delete_single_stock(stock_id)
        logger.info(f"Received DELETE /api/stock/<int:stock_id> with output: {result}")

        if result:
            logger.info(f"Stock with ID {stock_id} deleted successfully")
            return jsonify({"message": f"Stock with ID {stock_id} deleted successfully"}), HTTPStatus.OK

        logger.info(f"Stock with ID {stock_id} not found")
        return jsonify({"error": f"Stock with ID {stock_id} not found"}), HTTPStatus.NOT_FOUND

    except Exception as e:
        logger.error(f"Type Error: {type(str(e))}. Error: {str(e)}")
        return jsonify({"error": "Unexpected error occurred", "details": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
