from http import HTTPStatus
from flask import Blueprint, jsonify, request

from yf_service.methods.strategy_methods import strategyDB_Client


strategy_bp = Blueprint("strategy", __name__)


@strategy_bp.route("/trades/<string:code>", methods=["GET"])
def get_code_trades(code):
    """
    API endpoint to get stock trade data from the database.
    """
    try:
        result = strategyDB_Client.get_trades_for_code(code=code)

        if result is not None:
            return jsonify(result), HTTPStatus.OK
        
        else:
            return jsonify({'error': f'No trades found for the given code {code}'}), HTTPStatus.NOT_FOUND

    except Exception as e:
        return jsonify({"error": "Unexpected error occurred", "details": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


@strategy_bp.route("/results/<string:code>", methods=["GET"])
def get_code_results(code):
    try:
        result = strategyDB_Client.get_results_for_code(code=code)

        if result is not None:
            return jsonify(result), HTTPStatus.OK
        
        else:
            return jsonify({'error': f'No strategy results were found for the given code {code}'}), HTTPStatus.NOT_FOUND

    except Exception as e:
        return jsonify({"error": "Unexpected error occurred", "details": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


@strategy_bp.route("/", methods=["POST"])
def add_strategy():
    try:
        data = request.json

        result = strategyDB_Client.add_strategy_for_code(json_data=data)

        if result:
            return jsonify({'message': f"Trades and Results recorded for {data.get('code')}"}), HTTPStatus.CREATED
        else:
            return jsonify({'message': f"Trades and Results already exist for {data.get('code')}"}), HTTPStatus.CONFLICT

    except ValueError as ve:
        return jsonify({"error": f"{str(ve)}"})
    
    except Exception as e:
        return jsonify({"error": "Unexpected error occurred", "details": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


@strategy_bp.route("/<string:code>", methods=["DELETE"])
def delete_strategy(code):
    try:
        result = strategyDB_Client.delete_strategy_for_code(code=code)

        if result:
            return jsonify({"message": f"Strategy information for stock {code} removed."}), HTTPStatus.OK
        else:
            return jsonify({"message": f"No strategy information recorded for stock {code}."}), HTTPStatus.NOT_FOUND

    except Exception as e:
        return jsonify({"error": "Unexpected error occurred", "details": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
