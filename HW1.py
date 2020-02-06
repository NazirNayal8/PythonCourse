import random

class Thing:
    def __init__(self,ticker):
        self.ticker = ticker

        
class Stock(Thing):
    def __init__(self,price,ticker):
        super().__init__(ticker)
        self.price = price

class MutualFund(Thing):
    def __init__(self,ticker):
        super().__init__(ticker)
        
class Portfolio:
    def __init__(self):
        self.cash = 0
        self.investmentList = {}
        self.investmentPrice = {}
        self.stockList = {}
        self.mutualFundList = {}
        self.historyList = []
   
    def __str__(self):
        string = "Cash %f"%(self.cash) 
        string += "\n"
        string += "Stock: \n"
        for s in self.stockList:
            if self.stockList[s] == 1:
                string += s + ": %d"%(self.investmentList[s]) + "\n"
        string += "\nMutual Fund:\n"
        for m in self.mutualFundList:
            if self.mutualFundList[m] == 1:
                string += m + ": %f"%(self.investmentList[m]) + "\n"
        return string
    
    def addCash(self,amount):
        self.cash += amount
        self.historyList.append("Adds %d Cash"%(amount))
        
    def withdrawCash(self,amount):
        if amount > self.cash:
            print("Error: withdrawal amount greater than current cash. Withdrawal aborted")
            return
        self.cash -= amount
        self.historyList.append("Withdraws %d Cash"%(amount))
    
    def buy(self,ticker,shares,price):
        investmentPrice = shares * price
        if investmentPrice > self.cash:
            print("Error: price of investment greater than available cash. Task aborted")
            return False
        if ticker in self.investmentList:
            self.investmentList[ticker] += shares
        else:
            self.investmentList[ticker] = shares
        self.investmentPrice[ticker] = price
        self.cash -= investmentPrice
        self.historyList.append("Buys %f share of %s"%(shares,ticker))
        return True
        
    def buyStock(self,shares,stock):
        success = self.buy(stock.ticker,shares,stock.price)
        if success :
            self.stockList[stock.ticker] = 1
    def buyMutualFund(self,share,mutualFund):
        success = self.buy(mutualFund.ticker,share,1)
        if success :
            self.mutualFundList[mutualFund.ticker] = 1
    def sell(self,ticker,share,price):
        if self.investmentList[ticker] < share:
            print("Error: required stock share quantity not enought to sell. Task aborted")
            return
        if not (ticker in self.investmentList):
            print("Error: no such investment exists. Task aborted")
        self.cash += price
        self.investmentList[ticker] -= share
        self.historyList.append("Sells %f share of %s"%(share,ticker))
        
    def sellStock(self,stockTicker,share):
        if not (stockTicker in self.investmentPrice):
            print("Error: No such ticker exists in investments. Task aborted")
            return
        price = self.investmentPrice[stockTicker]
        soldPrice = random.uniform(0.5 * price,1.5 * price)
        self.sell(stockTicker,share,soldPrice)
        if self.investmentList[stockTicker] == 0:
            self.stockList[stockTicker] = 0
        
    def sellMutualFund(self,mutualFundTicker,share):
        if not (mutualFundTicker in self.investmentPrice):
            print("Error: No such ticker exists in investments. Task aborted")
            return
        price = random.uniform(0.9,1.2)
        self.sell(mutualFundTicker,share,price)
        if self.investmentList[mutualFundTicker] == 0:
            self.mutualFundList[mutualFundTicker] = 0
    def history(self):
        for E in self.historyList:
            print(E)


portfolio = Portfolio()
portfolio.addCash(300.50)
print(portfolio.cash)
print()
s = Stock(20, "HFH")
portfolio.buyStock(5, s)
print(portfolio.cash)
mf1 = MutualFund("BRT")
mf2 = MutualFund("GHT")
portfolio.buyMutualFund(10.3, mf1)
print(portfolio.cash)
portfolio.buyMutualFund(2, mf2)
print(portfolio.cash)
print(portfolio)
portfolio.sellMutualFund("BRT", 3)
print(portfolio.cash)
portfolio.sellStock("HFH", 1)
print(portfolio.cash)
portfolio.withdrawCash(50)
print(portfolio.cash)
portfolio.history()
print(portfolio.cash)
            
