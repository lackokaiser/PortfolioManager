from flask import Flask, jsonify, render_template, request
from dal.data import DatabaseAccess
import json
import pandas as pd
import functools
from viewmodel.feed import FeedItem
from viewmodel.ticker import TickerHistory
from dal.finance_api import FinanceAPI

app = Flask("PortfolioManagerAPI")
finance_api = FinanceAPI()
database = DatabaseAccess(finance_api)

@functools.cache
def get_ticker_list():
    ticker_pd= pd.read_csv("static/assets/all_tickers.csv")
    return ticker_pd[['Symbol', 'Name', 'Sector', 'Country']].fillna('Unknown')

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/market")
def market():
    return render_template("market_view.html")    

@app.route("/portfolio")
def about():
    tickers_df = get_ticker_list()
    stocks = json.loads(tickers_df.to_json(orient="records"))
    return render_template("portfolio_view.html",stocks=stocks)

@app.route("/history")
def history():
    return render_template("history.html")

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
    

    result = [FeedItem(item['ticker'], item['name'], finance_api.get_current_value(item['ticker']),
                       database.get_owned_stock(item['ticker'])[0][2], database.get_stock_pnl(item['ticker']), database.get_owned_stock_value(item['ticker'])) for item in feed_data]
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
    period = period_map.get(mode, '1d')

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
    app.run(debug=True, host="0.0.0.0")
