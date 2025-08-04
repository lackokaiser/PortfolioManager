from flask import Flask, jsonify, request,send_file
import yfinance as yf
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
ß
app = Flask(__name__)

def get_history_data(ticker, start, end, interval):
    ticker_obj = yf.Tickers(ticker)
    data = ticker_obj.history(
        start=start,
        end=end,
        interval=interval
    )
    return data.reset_index().to_dict(orient="records")

# def get_point

@app.route("/api/v1/stock/<ticker>/history")
def api_history(ticker):
    period = request.args.get("period", "1y") 
    interval = request.args.get("interval", "1d")

    ticker_data = yf.Ticker(ticker)
    historical_data = ticker_data.history(period=period,interval=interval)

    if historical_data.empty:
        return "No data available for this range.", 404

    # Graph
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(historical_data.index, historical_data['Close'], label='Close Price')
    ax.set_title(f"{ticker} Historical Close Price")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price (USD)")
    ax.legend()
    ax.grid(True)
    
    # Return graph as image
    img = io.BytesIO()
    plt.savefig(img, format='png')
    plt.close(fig)
    img.seek(0)
    return send_file(img, mimetype='image/png')

if __name__ == "__main__":
    app.run(debug=True)


