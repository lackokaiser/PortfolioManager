from flask import Flask, jsonify
from dal.data import DatabaseAccess
from viewmodel.feed import FeedItem
from viewmodel.ticker import TickerHistory
from dal.finance_api import FinanceAPI

app = Flask("PortfolioManagerAPI")
finance_api = FinanceAPI()
database = DatabaseAccess(finance_api)

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
                       database.get_owned_stock(item['ticker'])[0][2], database.get_stock_pnl(item['ticker'])) for item in feed_data]
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
    print(history_data)
    historyList = [item for item in history_data] 
    result = TickerHistory(ticker, historyList, historyList[0]['Date'], historyList[-1]['Date'])
    return jsonify(result)
 
@app.route("/api/v1/stock/<ticker>/buy/<amount>")
def buy_stock(ticker, amount):
    """
    Buys stock from the given ticker, returns true if the operation succeded, returns false otherwise
    """
    try:
        return jsonify(database.buy_stock(ticker, amount))
    except:
        return jsonify(False)

@app.route("/api/v1/stock/<ticker>/sell/<amount>")
def sell_stock(ticker, amount):
    return jsonify(database.sell_stock(ticker, amount))

if __name__ == "__main__":
    app.run()
    
    del database
    del finance_api