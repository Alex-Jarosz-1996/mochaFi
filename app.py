from flask import Flask, request, jsonify
from flask_app.core.yf_core import get_yf_stock_data

app = Flask(__name__)

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
