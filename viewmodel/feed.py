class FeedItem(dict):
    """Represents an object holding the data to be sent to the client.
    
    The object holds: Ticker, Current price, Current Profit, Volumes owned
    """
    def __init__(self, ticker: str, name: str, currentPrice: float, transactions: list[(str, float, float)], pnl: float, currentValue: float):
        self.ticker = ticker
        self.name = name
        self.currentPrice = currentPrice
        self.pnl = pnl
        self.volumeCount = self._get_total_volumes(transactions)
        self.currentValue = currentValue
        
        dict.__init__(self, ticker=ticker, name=name, currentPrice=currentPrice, transactions=transactions, pnl=pnl, volumeCount=self.volumeCount, currentValue=currentValue)
    
    def _get_total_volumes(self, transactions):
        """Calculates the total volume of shares owned based on transactions."""        
        return sum(float(item[1]) for item in transactions)