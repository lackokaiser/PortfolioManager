import yfinance as yf

class FinanceAPI:
    def get_feed(self, tickers, close=False):
        data = []
        stocks = yf.Tickers(tickers)
        for ticker in tickers:
            info = stocks.tickers[ticker].info

            # calculating the price growth
            current = info.get("regularMarketPrice", 0)
            previous = info.get("previousClose", 1) 
            growth = (current - previous) / previous

            # stock info
            data.append({
                "ticker": ticker,
                "name": info.get("shortName", ""),
                "price": current,
                "previous_close": previous,
                "growth": growth
            })
        return data
    

    def get_history(self, ticker, period='1wk'):
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period, interval=("1d" if period != "1d" else "2m"))

        hist = hist.reset_index().to_dict(orient="records")
        if period == '1d':
            for item in hist:
                item['Date'] = item['Datetime']
                item.pop('Datetime')

        # return data as list of dictionaries
        return hist

    def is_ticker_valid(self, ticker):
        tic = yf.Ticker(ticker)
        history = tic.history(period="1d")
        return len(history) != 0

    def get_current_value(self, ticker) -> float:
        tic = yf.Ticker(ticker)
        history = tic.history()
        if len(history) == 0:
            return 0.0
        return history["Close"].iloc[-1]
    
<<<<<<< HEAD
=======
    

>>>>>>> 04a6aaa9e1a30508525d270ed27f4ae76fc495f8
if __name__ == "__main__":
    fin = FinanceAPI()
    
    print(fin.get_current_value("AMZN"))