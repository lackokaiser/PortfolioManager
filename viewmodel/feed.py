class FeedItem:
    """Represents an object holding the data to be sent to the client.
    
    The object holds: Ticker, Current price, Current Profit, Volumes owned
    """
    def __init__(self, ticker: str, currentPrice: float, transactions: list[(str, float, float)], currentProfit: float):
        self.ticker = ticker
        self.currentPrice = currentPrice
        self.currentProfit = currentPrice
        self.volumeCount = self._get_total_volumes(transactions)
    
    def _get_total_volumes(self, transactions):
        res = 0
        
        for item in transactions:
            res = res + item[1]
        
        return res