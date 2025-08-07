from flask import Flask, jsonify, render_template, request
import yfinance as yf

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

<<<<<<< HEAD
@app.route("/stocks")
def get_stocks():
    symbols_param = request.args.get("symbols", " ")
    
    if not re.match(r'^([A-Za-z] +,)*[A-Za-z]+$', symbols_param):
        return jsonify({"error": "Invalid symbols format"}), 400
    
    symbols = symbols_param.split(",")
    results = []
    
    for symbol in symbols:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="1d")
        
        if hist.empty:
            continue
        
        latest = hist.iloc[-1]
        date = hist.index[-1].strftime('%y=%m-%d')
        
        results.append = ({
            "Symbol": symbol,
            "Date": date,
            "Open": round(latest["Open"], 2),
            "High": round(latest["High"], 2),
            "Low": round(latest["Low"], 2),
            "Close": round(latest["Close"], 2),
            "Volume": int(latest["Volume"])
            })
        
        return jsonify(results)
    
    if __name__ == "__main__":
=======

@app.route("/stocks/<symbols>")
def stock_data(symbol):
    period = request.args.get("period", "5d")
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period=period)
    return jsonify(hist.reset_index().to_dict(orient="records"))

if __name__ == "__main__":
>>>>>>> 04a6aaa9e1a30508525d270ed27f4ae76fc495f8
        app.run(debug=True)