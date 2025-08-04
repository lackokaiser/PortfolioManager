import unittest
from dal.data import DatabaseAccess

db = DatabaseAccess(None)

class TestSQL(unittest.TestCase):
    def test_owned_stock(self):
        result = db.get_owned_stock()
        
        print(result)
    
    def test_transactions(self):
        self.assertTrue(db.buy_stock("AMZNtest", 2))
        
        self.assertEqual(db.get_stock_amount("AMZNtest"), 2)
        
        self.assertTrue(db.sell_stock("AMZNtest", 2))
        
        self.assertEqual(db.get_stock_amount("AMZNtest"), 0)
        
    def test_pnl(self):
        self.assertTrue(db.buy_stock("AMZNtest", 2))
        
        self.assertEqual(db.get_stock_pnl("AMZNtest"), 10)
        
        self.assertTrue(db.buy_stock("AMZNtest", 3))
        
        self.assertEqual(db.get_stock_pnl("AMZNtest"), 25)
        
        self.assertTrue(db.sell_stock("AMZNtest", 5))
        
        self.assertEqual(db.get_stock_pnl("AMZNtest"), 0)

if __name__ == "__main__":
    unittest.main()