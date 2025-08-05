from flask import Flask, jsonify, session, request,render_template, g, redirect, url_for, flash
from flask_restful import Resource, Api,fields
import json, pandas as pd
import mysql.connector
import yfinance as yf
import functools
import dal.data as dataClass
from dal.finance_api import FinanceAPI

app = Flask("api")
api = Api(app)
fin = FinanceAPI()


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

@app.route("/api/v1/stock/<ticker>/point")
def get_point_data(ticker):
    return jsonify({ticker: fin.get_current_value(ticker)})

@app.route("/api/v1/<ticker>/sell/<amount>")
def sell_stock(ticker, amount):
    accessLayer.sell_stock(ticker, amount)
    return jsonify({"message": f"Sold {amount} shares of {ticker}"}), 200

@app.route("/api/v1/<ticker>/buy/<amount>") 
def buy_stock(ticker, amount):
    accessLayer.buy_stock(ticker, amount)
    return jsonify({"message": f"Bought {amount} shares of {ticker}"}), 200

# @app.route("/api/v1/portfolio")
# def get_portfolio():
#     try:
#         portfolio = accessLayer.get_owned_stock()
#         print(f"Portfolio data: {portfolio}")
#         return jsonify(portfolio)
#     except Exception as e:
#         print(f"Error fetching portfolio: {e}")
#         return jsonify({"Could not fetch portfolio": e}), 500
    
class getPortfolio(Resource):
    # Adding the default get method with caching
    # This method saves the data in the cache for faster access
    @functools.cache
    def get(self):
        passCursor = accessLayer.dbConnection.cursor(dictionary=True)
        passCursor.execute("SELECT * FROM stockdemo order by ticker")
        passwords = passCursor.fetchall()
        passCursor.close()
        return jsonify(passwords)


if __name__ == "__main__":
    try:
        accessLayer = dataClass.DatabaseAccess(None)
        api.add_resource(getPortfolio, '/api/v1/portfolio')
        app.run(debug=True, host="0.0.0.0")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Close the database connection when the application terminates
        accessLayer.__del__()

