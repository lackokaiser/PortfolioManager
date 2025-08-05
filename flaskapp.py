from flask import Flask, jsonify
from dal.data import DatabaseAccess
from viewmodel.feed import FeedItem
from viewmodel.ticker import TickerHistory
from dal.finance_api import FinanceAPI
import yfinance as yf

app = Flask("PortfolioManagerAPI")
finance_api = FinanceAPI()
database = DatabaseAccess(finance_api)


@app.route("/api/v1/stock/<ticker>/point")
def get_point_data(ticker):
    data = yf.download(ticker,period="1d")
    data = data['Close']
    print(jsonify())
    return jsonify(data.to_dict(orient="records"))

@app.route("/api/v1/portfolio")
def get_portfolio():
    """
    Returns the portfolio of the user
    """
    portfolio = database.get_stock_pnl()
    if not portfolio:
        return jsonify([]), 200
    
    result = [TickerHistory(**item).to_dict() for item in portfolio]
    return jsonify(result)

        
@app.route("/api/v1/stock/feed")
@app.route("/api/v1/stock/feed/<ticker>")
def load_feed(ticker = None):
    """
    Should return a sorted list of stocks containing our own tracked items as well
    
    Order should be based on: Owned stocks, stock price growth
    """
    tickers = database.get_owned_tickers() 
    if ticker:
        tickers.append(ticker.upper())

    tickers = list(set(tickers))  
    feed_data = finance_api.get_feed(tickers)

    feed_data.sort(key=lambda x: (x["ticker"] not in database.get_owned_tickers(), -x["growth"]))

    result = [FeedItem(**item).to_dict() for item in feed_data]
    return jsonify(result)
   
@app.route("/api/v1/stock/<ticker>/history/<mode>")
@app.route("/api/v1/stock/<ticker>/history")
def get_history(ticker, mode='w'):
    """
    Should return a history to the caller
    """
    period_map = {
        'd': '1d',
        'w': '1wk',
        'm': '1mo'
    }
    period = period_map.get(mode, '1wk')

    history_data = finance_api.get_history(ticker.upper(), period)
    result = [TickerHistory(**item).to_dict() for item in history_data]
    return jsonify(result)
 
@app.route("/api/v1/stock/<ticker>/buy/<amount>")
def buy_stock(ticker, amount):
    """
    Buys stock from the given ticker, returns true if the operation succeded, may not return anything otherwise
    """
    return jsonify(database.buy_stock(ticker, amount))

@app.route("/api/v1/stock/<ticker>/sell/<amount>")
def sell_stock(ticker, amount):
    return jsonify(database.sell_stock(ticker, amount))

if __name__ == "__main__":
    app.run()