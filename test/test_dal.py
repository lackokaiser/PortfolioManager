import unittest
from dal.data import DatabaseAccess
from dal.finance_api import FinanceAPI

fin = FinanceAPI()
db = DatabaseAccess(fin)

class TestSQL(unittest.TestCase):
    def test_owned_stock(self):
        result = db.get_owned_stock()
        
        print(result)
    
    def test_transactions(self):
        self.assertTrue(db.buy_stock("AMZN", 2))
        
        self.assertEqual(db.get_stock_amount("AMZN"), 2)
        
        self.assertTrue(db.sell_stock("AMZN", 2))
        
        self.assertEqual(db.get_stock_amount("AMZN"), 0)
        
    def test_pnl(self):
        self.assertTrue(db.buy_stock("AMZN", 2))
        
        self.assertAlmostEqual(db.get_owned_stock_value("AMZN"), fin.get_current_value("AMZN") * 2)
        
        self.assertTrue(db.buy_stock("AMZN", 3))
        
        self.assertAlmostEqual(db.get_owned_stock_value("AMZN"), fin.get_current_value("AMZN") * 5)
        
        self.assertTrue(db.sell_stock("AMZN", 5))
        
        self.assertAlmostEqual(db.get_owned_stock_value("AMZN"), 0)
    
    def test_owned_ticker(self):
        self.assertTrue(db.buy_stock("NVDA", 2))
        tickers = db.get_owned_tickers()
        self.assertEqual(len(tickers), 1)
        self.assertEqual(tickers[0], "NVDA")
        self.assertTrue(db.sell_stock("NVDA", 2))
        tickers = db.get_owned_tickers()
        self.assertEqual(len(tickers), 0)
        

if __name__ == "__main__":
    unittest.main()