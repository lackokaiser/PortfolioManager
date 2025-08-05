from viewmodel.feed import FeedItem
from datetime import datetime

class TickerHistory(dict):
    """
    Represents an object holding the history of a ticker
    """
    
    def __init__(self, ticker: str, history: list[float], fromDate: datetime, toDate: datetime):
        self.ticker = ticker
        self.history = history
        self.fromDate = fromDate
        self.toDate = toDate
        
        dict.__init__(self, ticker=ticker, history=history, fromDate=fromDate, toDate=toDate)

class TickerProfile(dict):
    """
    Represents the object holding the detailed information about the ticker
    """
    
    def __init__(self, feedItem: FeedItem, transactions: list[(str, float, float)], history: TickerHistory):
        self.ticker = feedItem.ticker
        self.feedItem = feedItem
        self.transactions = transactions
        self.history = history
        
        dict.__init__(feedItem=feedItem, transactions=transactions, history=history)
