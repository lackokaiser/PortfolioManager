from flask import Flask, jsonify, request
from datetime import datetime, timedelta
import yfinance as yf

app = Flask(__name__)

def get_history_data(ticker, start, end, interval):
    ticker_obj = yf.Tickers(ticker)
    data = ticker_obj.history(
        start=start,
        end=end,
        interval=interval
    )
    return data.reset_index().to_dict(orient="records")

@app.route("/api/v1/stock/<ticker>/history")
def api_history(ticker):
    today = datetime.today()
    default_start = (today - timedelta(days=365)).strftime("%Y-%m-%d")
    default_end = today.strftime("%Y-%m-%d")
    default_interval = "1d"

    # Use defaults if not provided
    start = request.args.get("start", default_start)
    end = request.args.get("end", default_end)
    interval = request.args.get("interval", default_interval)

    data_json = get_history_data(ticker, start, end, interval)
    return jsonify({"ticker": ticker, "history": data_json})

if __name__ == "__main__":
    app.run(debug=True)