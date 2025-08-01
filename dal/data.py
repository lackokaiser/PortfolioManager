import mysql.connector

class DatabaseAccess:
    
    def __init__(self, financeInstance):
        self.dbConnection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="n3u3da!",
            database="CSFoundations"
        )
        self.yFinance = financeInstance
    
    def get_owned_stock(self, ticker = None):
        curs = self.dbConnection.cursor()
        
        if ticker == None:
            curs.execute("select * from stockdemo order by ticker")
        else:
            curs.execute(f"select * from stockdemo where ticker = '{ticker}'")
        fetch = curs.fetchall()
        curs.close()
        
        if len(fetch) == 0:
            return []
        
        item = fetch[0]
        
        res = [(item[1], [(item[5], item[4], item[3])])]
        
        curr_ind = 0
        i = 1
        while(i < len(res)):
            while i < len(res) and fetch[i][0] == res[curr_ind][0]:
                item = fetch[i]
                res[curr_ind][1].append((item[5], item[4], item[3]))
                i = i + 1
            item = fetch[i]
            curr_ind = curr_ind + 1
            res.append((item[1], [(item[5], item[4], item[3])]))
            
        return res        
        
    def sell_stock(self, ticker, amount) -> bool:
        if self.get_stock_amount(ticker) < amount:
            return False
        
        self.buy_stock(ticker, -amount)
        return True
        
    def buy_stock(self, ticker: str, amount: float):
        curs = self.dbConnection.cursor()
        
        curs.execute(f"insert into stockdemo (ticker, stock_name, stock_value, quantity) values ('{ticker}', '', {self._get_value(ticker)}, {amount})")
        self.dbConnection.commit()
        curs.close()
    
    def _get_value(self, ticker) -> float:
        return 5  # TODO yahoo call
    
    def get_stock_pnl(self, ticker):
        curs = self.dbConnection.cursor()
        
        curs.execute(f"select ticker, sum(quantity), sum(stock_value * quantity) from stockdemo where ticker = '{ticker}' group by ticker")
        
        data = curs.fetchall()
        curs.close()
        currentPrice = 10 # TODO add call to yahoo
        
        if len(data) == 0:
            return 0
        
        sum_quantity = data[0][1]
        sum_value = data[0][2]
        
        sell_price = sum_quantity * currentPrice
        
        return sell_price - sum_value
    
    def get_stock_amount(self, ticker) -> int:
        data = self.get_owned_stock()
        
        if len(data) == 0:
            return 0
        
        ind = 0
        
        while data[ind][0] != ticker:
            ind = ind + 1
        
        count = 0
        
        for item in data[ind][1]:
            count = count + item[4]
        
        return count
    
    def __del__(self):
        if self.dbConnection:
            self.dbConnection.close()
    
    

if __name__ == "__main__":
    
    da = DatabaseAccess(None)

    da.buy_stock(ticker="Hehe", amount=3)

    print(da.get_stock_pnl("Hehe"))