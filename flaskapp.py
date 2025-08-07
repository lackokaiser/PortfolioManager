from flask import Flask, jsonify, render_template, request
from dal.data import DatabaseAccess
import json
import yfinance as yf
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


@app.route("/market")
def market():
    return render_template("market_view.html")    

@app.route("/")
@app.route("/home")
@app.route("/portfolio")
def about():
    tickers_df = get_ticker_list()
    stocks = json.loads(tickers_df.to_json(orient="records"))
    return render_template("portfolio_view.html",stocks=stocks)

@app.route("/history")
def history():
    return render_template("history.html")

@functools.lru_cache(maxsize=128)  
@app.route("/api/v1/stock/<ticker>/point")
def get_point_data(ticker):
    return jsonify([{ticker: finance_api.get_current_value(ticker)}])

@functools.lru_cache(maxsize=128)  
@app.route("/api/v1/stock/feed")
def load_feed():
    """
    Should return a sorted list of stocks containing our own tracked items as well
    
    Order should be based on: Owned stocks, stock price growth
    """
    owned_tickers = database.get_owned_tickers()
    tickers = [item for item in owned_tickers]

    tickers = list(set(tickers))  
    feed_data = finance_api.get_feed(tickers)
    
    feed_data.sort(key=lambda x: (x["ticker"] not in owned_tickers, -x["growth"]))
    
    pnl_dict = database.get_all_stock_pnl()
    owned = database.get_owned_stock()
    
    def sum_count(transactions):
        res = 0.0
        for item in transactions:
            res = res + item[1]
        return res

    def find_tuple(owned, ticker):
        for item in owned:
            if item[0] == ticker:
                return item
        return None
    result = []
    for item in feed_data:
        owned_stock = find_tuple(owned, item['ticker'])
        result.append(FeedItem(item['ticker'], item['name'], item['price'],
                       owned_stock[2], pnl_dict[item['ticker']], item['price'] * sum_count(owned_stock[2])))

    return jsonify(result)
   
@functools.lru_cache(maxsize=128)  
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
    result = TickerHistory(ticker, history_data, history_data[0]['Date'], history_data[-1]['Date'])
    return jsonify(result)
 
@app.route("/api/v1/stock/<ticker>/buy/<float:amount>")
@app.route("/api/v1/stock/<ticker>/buy/<int:amount>")
def buy_stock(ticker, amount):
    """
    Buys stock from the given ticker, returns 200 if the operation succeeded, may not return anything otherwise
    """
    return jsonify(database.buy_stock(ticker, amount))

@app.route("/api/v1/stock/<ticker>/sell/<float:amount>")
@app.route("/api/v1/stock/<ticker>/sell/<int:amount>")
def sell_stock(ticker, amount):
    return jsonify(database.sell_stock(ticker, amount))

@app.route("/api/v1/portfolio")
def get_portfolio_performance():
    """
    Returns the current portfolio performance
    """
    try:
        owned_tickers = database.get_owned_tickers()
        stocks = yf.Tickers(owned_tickers).download(period='1wk', auto_adjust=True)
        day_performance = stocks.Close
        df = database.get_transaction_history()
        cumulative_holdings = database.calculate_cumulative_holdings(df)
        cumulative_valuation = cumulative_holdings.multiply(day_performance, axis=0,fill_value=1).sum(axis=1)
        cumulative_valuation.columns = ['Date', 'Cumulative Valuation']
        print(f"Cumulative valuation: {json.dumps(cumulative_valuation)}")
        return jsonify(cumulative_valuation.to_dict(orient='records'))
    except Exception as e:
        print(f"Error fetching portfolio: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
