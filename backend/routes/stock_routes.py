from http import HTTPStatus
from flask import Blueprint, jsonify, request

from sqlalchemy.exc import IntegrityError

from schema.stock_schema import StockSchema
from yf_service.methods.stock_methods import stockDB_Client


stock_bp = Blueprint("stock", __name__)


@stock_bp.route("/", methods=["GET"])
def get_stocks():
    """
    API endpoint to get all stocks from the database.
    """
    try:
        result = stockDB_Client.get_all_stocks()
        
        if result is not None:
            if isinstance(result, list):
                return jsonify(StockSchema(many=True).dump(result)), HTTPStatus.OK
            else:
                return jsonify(StockSchema().dump(result)), HTTPStatus.OK
        
        return jsonify({"error": "No stocks found"}), HTTPStatus.NOT_FOUND
    
    except Exception as e:
        return jsonify({"error": "Failed to fetch stocks", "details": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


@stock_bp.route("/", methods=["POST"])
def add_stock():
    """
    API endpoint to add a single stock to the database.
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Invalid or missing JSON data"}), HTTPStatus.BAD_REQUEST

        result = stockDB_Client.add_single_stock(json_data=data)

        if result:
            return jsonify({"message": f"Stock {data.get('code')} successfully"}), HTTPStatus.OK
    
    except ValueError as ve:
        return jsonify({"error": str(ve)}), HTTPStatus.CONFLICT

    except TypeError as te:
        return jsonify({"error": str(te)}), HTTPStatus.INTERNAL_SERVER_ERROR

    except IntegrityError:
        return jsonify({"error": f"Stock {data.get('code')} already added."}), HTTPStatus.INTERNAL_SERVER_ERROR
    
    except Exception as e:
        print(type(e))
        return jsonify({"error": "Unexpected error occurred", "details": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


@stock_bp.route("/", methods=["DELETE"])
def delete_all_stocks():
    """
    API endpoint to remove all stocks from the database.
    """
    try:
        result = stockDB_Client.delete_all_stocks()

        if result:
            return jsonify({"message": "All stocks deleted successfully"}), HTTPStatus.OK

        return jsonify({"message": "No stocks to delete"}), HTTPStatus.NOT_FOUND

    except Exception as e:
        return jsonify({"error": "Unexpected error occurred", "details": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


@stock_bp.route("/<int:stock_id>", methods=["DELETE"])
def delete_stock(stock_id):
    """
    API endpoint to remove single stock from the database.
    """
    try:
        result = stockDB_Client.delete_single_stock(stock_id)

        if result:
            return jsonify({"message": f"Stock with ID {stock_id} deleted successfully"}), HTTPStatus.OK

        return jsonify({"error": f"Stock with ID {stock_id} not found"}), HTTPStatus.NOT_FOUND

    except Exception as e:
        return jsonify({"error": "Unexpected error occurred", "details": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
