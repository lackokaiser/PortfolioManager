from flask import Flask, jsonify
from dal.data import DatabaseAccess
from viewmodel.feed import FeedItem
from viewmodel.ticker import TickerHistory

app = Flask("PortfolioManagerAPI")
database = DatabaseAccess()

@app.route("/api/v1/stock/feed")
@app.route("/api/v1/stock/feed/<ticker>")
def load_feed(ticker = None):
    """
    Should return a sorted list of stocks containing our own tracked items as well
    
    Order should be based on: Owned stocks, stock price growth
    """
    # TODO: Doyin's wrapper api is needed here, use FeedItem
    pass
   
@app.route("/api/v1/stock/<ticker>/history/<mode>")
@app.route("/api/v1/stock/<ticker>/history")
def get_history(ticker, mode='w'):
    """
    Should return a history to the caller
    """
    # TODO: Doyin's wrapper api is needed here, use TickerHistory
    pass
 
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