from flask import Flask, jsonify, render_template, request
import yfinance as yf

app = flask(__name__)

@app.route("/")
def index():
    return render_template("market.html")

@app.route("/stocks")
def get_stocks():
    symbols_param = request.args.get("symbols", " ")
    
    if not re.match(r'^([A-Za-z] +,)*[A-Za-z]+$', symbols_param):
        return jsonify({"error": "Invalid symbols format"}), 400
    
    symbols = symbols_param.split(",")
    results = []
    
    for symbol in symbols:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="1mo")
        
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
        app.run(debug=True)