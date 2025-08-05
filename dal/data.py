import mysql.connector
from datetime import date
from dal.finance_api import FinanceAPI

class DatabaseAccess:
    
    def __init__(self, financeInstance: FinanceAPI):
        self.dbConnection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="n3u3da!",
            database="CSFoundations"
        )
        self.yFinance = financeInstance
    
    def _sanitize_value(self, value: str):
        """_summary_: Validates and sanitizes the value against sql injection
        Args:
            value (_type_): _description_: The string value
        """
        
        return ''.join(c for c in value if c.isdecimal() or c.isalpha())
    
    def get_owned_stock(self, ticker = None) -> list[tuple[str, str, list[tuple[date, float, float]]]]:
        """
        [('AMZN', 'Amazon corp' [(datetime.date(2025, 8, 1), Decimal('1'), Decimal('0'))])]
        Ticker,   Name,         transaction date,             quantity,     buying price
        """
        curs = self.dbConnection.cursor()
        
        if ticker == None:
            curs.execute("select * from stockdemo order by ticker")
        else:
            curs.execute(f"select * from stockdemo where ticker = '{self._sanitize_value(ticker)}'")
        fetch = curs.fetchall()
        curs.close()
        
        if len(fetch) == 0:
            return []
        
        item = fetch[0]
        
        res = [(item[1], item[2], [(item[5], item[4], item[3])])]
        
        curr_ind = 0
        i = 1
        while(i < len(fetch)):
            while i < len(fetch) and fetch[i][1] == res[curr_ind][0]:
                item = fetch[i]
                res[curr_ind][2].append((item[5], item[4], item[3]))
                i = i + 1
            if i >= len(fetch):
                continue
            item = fetch[i]
            curr_ind = curr_ind + 1
            res.append((item[1], item[2], [(item[5], item[4], item[3])]))
            
        return res        
        
    def sell_stock(self, ticker, amount, name="") -> bool:
        amount = self.get_stock_amount(ticker)
        if self.get_stock_amount(ticker) < amount:
            return False
        
        return self.buy_stock(ticker, amount * -1, name=name)
        
    def buy_stock(self, ticker: str, amount: float, name="") -> bool:
        curs = self.dbConnection.cursor()
        
        curs.execute(f"insert into stockdemo (ticker, stock_name, stock_value, quantity) values ('{self._sanitize_value(ticker)}', '{self._sanitize_value(name)}', {self._get_value(ticker)}, {amount})")
        self.dbConnection.commit()
        curs.close()
        return True
    
    def _get_value(self, ticker) -> float:
        return self.yFinance.get_current_value(ticker)
    
    def get_stock_pnl(self, ticker):
        curs = self.dbConnection.cursor()
        
        curs.execute(f"select ticker, sum(quantity), sum(stock_value * quantity) from stockdemo where ticker = '{self._sanitize_value(ticker)}' group by ticker")
        
        data = curs.fetchall()
        curs.close()
        currentPrice = self._get_value(ticker)
        
        if len(data) == 0:
            return 0
        
        sum_quantity = data[0][1]
        sum_value = data[0][2]
        
        sell_price = sum_quantity * currentPrice
        
        return sell_price - sum_value

    def get_stock_amount(self, ticker) -> int:
        curs = self.dbConnection.cursor()
        
        curs.execute(f"select sum(quantity) from stockdemo where ticker = '{self._sanitize_value(ticker)}'")
        
        data = curs.fetchall()
        curs.close()
        
        return data[0][0]
        
    def get_owned_tickers(self):
        curs = self.dbConnection.cursor()
        
        curs.execute("select distinct ticker from stockdemo")
        
        data = curs.fetchall()
        curs.close()
        
        res = [item[0] for item in data if self.get_stock_amount(item[0]) > 0]
        
        return res
    
    
    
    def __del__(self):
        if self.dbConnection:
            self.dbConnection.close()
    
    

if __name__ == "__main__":
    
    da = DatabaseAccess(FinanceAPI())
    
    da.get_owned_tickers()
    
    del da