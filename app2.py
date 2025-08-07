from flask import Flask, jsonify, render_template, request
import yfinance as yf

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/stocks/<symbols>")
def stock_data(symbol):
    period = request.args.get("period", "5d")
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period=period)
    return jsonify(hist.reset_index().to_dict(orient="records"))

if __name__ == "__main__":
        app.run(debug=True)