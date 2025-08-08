class FeedItem(dict):
    """Represents an object holding the data to be sent to the client.
    
    The object holds: Ticker, Current price, Current Profit, Volumes owned
    """
    def __init__(self, ticker: str, name: str, currentPrice: float, transactions: list[(str, float, float)], pnl: float, currentValue: float):
        self.ticker = ticker
        self.name = name
        self.currentPrice = round(float(currentPrice), 2)
        self.pnl = round(float(pnl), 2)
        self.volumeCount = round(self._get_total_volumes(transactions), 3)
        self.currentValue = round(float(currentValue), 2)
        
        dict.__init__(self, 
                            ticker=ticker, 
                            name=name, 
                            currentPrice=self.currentPrice,  
                            pnl=self.pnl,                  
                            volumeCount=self.volumeCount,  
                            currentValue=self.currentValue) 
        
    def _get_total_volumes(self, transactions):
        """Calculates the total volume of shares owned based on transactions."""        
        if not transactions:
            return 0.0
        return sum(float(item[1]) for item in transactions)