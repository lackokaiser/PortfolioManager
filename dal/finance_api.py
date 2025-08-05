import yfinance as yf

class FinanceAPI:
    def get_feed(self, tickers):
        data = []
        for ticker in tickers:
            stock = yf.Ticker(ticker)
            info = stock.info

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
        hist = stock.history(period=period)

        # return data as list of dictionaries
        return hist.reset_index().to_dict(orient="records")

    def get_current_value(self, ticker) -> float:
        tic = yf.Ticker(ticker)
        history = tic.history()
        return history["Close"].iloc[-1]

if __name__ == "__main__":
    fin = FinanceAPI()
    
    print(fin.get_current_value("AMZN"))