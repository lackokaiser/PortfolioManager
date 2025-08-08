import yfinance as yf

class FinanceAPI:
    def get_feed(self, tickers, close=False):
        if not tickers:
            return []
            
        data = []
        # Get all ticker data in one call for better performance
        stocks = yf.Tickers(tickers)
        
        # Download all data at once instead of individual calls
        try:
            hist_data = stocks.download(period="1d", auto_adjust=True)
            current_prices = hist_data['Close'].iloc[-1] if len(hist_data) > 0 else {}
            previous_prices = hist_data['Close'].iloc[-2] if len(hist_data) > 1 else {}
        except:
            current_prices = {}
            previous_prices = {}
        
        for ticker in tickers:
            try:
                info = stocks.tickers[ticker].info
                
                # Use downloaded data if available, otherwise fall back to info
                current = current_prices.get(ticker, info.get("regularMarketPrice", 0))
                previous = previous_prices.get(ticker, info.get("previousClose", current))
                
                if previous == 0:
                    previous = current
                    
                # growth = (current - previous) / previous if previous != 0 else 0

                data.append({
                    "ticker": ticker,
                    "name": info.get("shortName", ticker),
                    "price": float(current),
                    "previous_close": float(previous),
                    "growth": 0.0
                })
            except Exception as e:
                print(f"Error getting data for {ticker}: {e}")
                # Add fallback data to prevent crashes
                data.append({
                    "ticker": ticker,
                    "name": ticker,
                    "price": 0.0,
                    "previous_close": 0.0,
                    "growth": 0.0
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
    
    

if __name__ == "__main__":
    fin = FinanceAPI()
    
    print(fin.get_current_value("AMZN"))