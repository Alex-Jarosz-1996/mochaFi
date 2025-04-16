from http import HTTPStatus
from flask import Blueprint, jsonify, request

from setup_logging.setup_logging import logger

from yf_service.methods.strategy_methods import strategyDB_Client


strategy_bp = Blueprint("strategy", __name__)


@strategy_bp.route("/trades/<string:code>", methods=["GET"])
def get_code_trades(code):
    """
    API endpoint to get stock trade data from the database.
    """
    try:
        logger.info("Executing GET /api/strategy/trades/<string:code> endpoint.")
        result = strategyDB_Client.get_trades_for_code(code=code)
        logger.info(f"Received GET /api/strategy/trades/<string:code>")

        if result is not None:
            logger.info("Trades found. Returning HTTP 200 Ok status.")
            return jsonify(result), HTTPStatus.OK
        
        else:
            logger.info(f'No trades found for the given code {code}')
            return jsonify({'error': f'No trades found for the given code {code}'}), HTTPStatus.NOT_FOUND

    except Exception as e:
        logger.error(f"Type Error: {type(str(e))}. Error: {str(e)}")
        return jsonify({"error": "Unexpected error occurred", "details": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


@strategy_bp.route("/results/<string:code>", methods=["GET"])
def get_code_results(code):
    try:
        logger.info("Executing GET /api/strategy/results/<string:code> endpoint.")
        result = strategyDB_Client.get_results_for_code(code=code)
        logger.info(f"Received GET /api/strategy/results/<string:code>")

        if result is not None:
            logger.info("Results found. Returning HTTP 200 Ok status.")
            return jsonify(result), HTTPStatus.OK
        
        else:
            logger.info(f'No strategy results were found for the given code {code}')
            return jsonify({'error': f'No strategy results were found for the given code {code}'}), HTTPStatus.NOT_FOUND

    except Exception as e:
        logger.error(f"Type Error: {type(str(e))}. Error: {str(e)}")
        return jsonify({"error": "Unexpected error occurred", "details": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


@strategy_bp.route("/", methods=["POST"])
def add_strategy():
    try:
        logger.info("Executing POST /api/strategy endpoint.")
        data = request.get_json()
        logger.info(f"Received POST /api/strategy with output: {data}")

        result = strategyDB_Client.add_strategy_for_code(json_data=data)
        logger.info(f"Result from strategyDB_Client.add_strategy_for_code: {result}")

        if result:
            logger.info(f"Trades and Results recorded for {data.get('code')}")
            return jsonify({'message': f"Trades and Results recorded for {data.get('code')}"}), HTTPStatus.CREATED
        else:
            logger.info(f"Trades and Results already exist for {data.get('code')}")
            return jsonify({'message': f"Trades and Results already exist for {data.get('code')}"}), HTTPStatus.CONFLICT

    except ValueError as ve:
        logger.error(f"Type Error: ValueError. Error: {str(ve)}")
        return jsonify({"error": f"{str(ve)}"})
    
    except Exception as e:
        logger.error(f"Type Error: {type(str(e))}. Error: {str(e)}")
        return jsonify({"error": "Unexpected error occurred", "details": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


@strategy_bp.route("/<string:code>", methods=["DELETE"])
def delete_strategy(code):
    try:
        logger.info("Executing DELETE /api/strategy/<string:code> endpoint.")
        result = strategyDB_Client.delete_strategy_for_code(code=code)
        logger.info(f"Received DELETE /api/strategy/<string:code> with output: {result}")

        if result:
            logger.info(f"Strategy information for stock {code} removed.")
            return jsonify({"message": f"Strategy information for stock {code} removed."}), HTTPStatus.OK
        else:
            logger.info(f"No strategy information recorded for stock {code}.")
            return jsonify({"message": f"No strategy information recorded for stock {code}."}), HTTPStatus.NOT_FOUND

    except Exception as e:
        logger.error(f"Type Error: {type(str(e))}. Error: {str(e)}")
        return jsonify({"error": "Unexpected error occurred", "details": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
