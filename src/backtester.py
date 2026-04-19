from constants import BUY, SELL, HOLD
from strategies import MovingAverage, MovingAverageConfig
from api_methods import fetch_historical_data
from dotenv import load_dotenv
from binance.client import Client
import os


"""
Buy & Sell Actions
"""
class Action:
    def __init__(self, type, price, timestamp, holdings):
        self.type = type
        self.price = price
        self.timestamp = timestamp
        self.holdings = holdings
        
    def handle_action(self, tester):
        raise NotImplementedError
    
class Buy(Action):
    def handle_action(self, tester):
        if tester.balance <= 0:
            self.spend = 0.0
            return
        
        self.spend = tester.balance
        fee_cost = tester.fee * self.spend
        tester.holdings = (self.spend - fee_cost) / self.price
        tester.balance = 0.0

class Sell(Action):
    def handle_action(self, tester):
        if tester.holdings <= 0:
            self.balance = 0.0
            return

        proceeds = tester.holdings * self.price
        fee_cost = proceeds * tester.fee
        tester.balance = proceeds - fee_cost
        self.balance = tester.balance
        tester.holdings = 0.0

"""
Back Testing Class
"""
class BackTester:
    def __init__(self, candles, starting_balance, fee):
        self.candles = candles
        self.balance = starting_balance
        self.starting_balance = starting_balance
        self.holdings = 0.0
        self.fee = fee
        self.trades = []
        self.equity_curve = []
    
    def current_equity(self, price):
        """
        Calucaltes total value: cash + value of any held position 
        """
        return self.balance + (self.holdings * price)
    
    def run(self, strategy):
        for i, candle in enumerate(self.candles):
            candles_up_to_i = self.candles[0:i+1]
            
            signal = strategy.generate_signal(candles_up_to_i)
            
            if signal == BUY and self.holdings == 0:
                buy = Buy(BUY, candle.close, candle.close_time, self.holdings)
                buy.handle_action(self)
                self.trades.append(buy)
                
            elif signal == SELL and self.holdings > 0:
                sell = Sell(SELL, candle.close, candle.close_time, self.holdings)
                sell.handle_action(self)
                self.trades.append(sell)
                
            self.equity_curve.append(self.current_equity(candle.close))
    
    def print_results(self):
        final_equity = self.current_equity(self.candles[-1].close)
        profit = final_equity - self.starting_balance
        pct_return = (profit / self.starting_balance) * 100

        buys = [trade for trade in self.trades if trade.type == BUY]
        sells = [trade for trade in self.trades if trade.type == SELL]

        wins = 0
        total_profit_loss = []

        for i, sell in enumerate(sells):
            if i < len(buys):
                trade_pl = sell.balance - buys[i].spend
                total_profit_loss.append(trade_pl)
                if trade_pl > 0:
                    wins += 1

        avg_pl = sum(total_profit_loss) / len(total_profit_loss) if total_profit_loss else 0

        print(f"Starting Balance : ${self.starting_balance:.2f}")
        print(f"Final Equity     : ${final_equity:.2f}")
        print(f"Net Profit       : ${profit:.2f}  ({pct_return:.1f}%)")
        print(f"Total Trades     : {len(self.trades)}")
        print(f"Buys             : {len(buys)}")
        print(f"Sells            : {len(sells)}")

        if len(sells) == 0:
            return

        print(f"Wins / Sells     : {wins}/{len(sells)} ({wins/len(sells)*100:.1f}%)")
        print(f"Avg P&L per trade: ${avg_pl:.2f}")
"""
Run Backtester script
"""
if __name__ == "__main__":
    # fetch data
    load_dotenv()
    client = Client(os.getenv("BINANCE_API_KEY"),os.getenv("BINANCE_SECRET_KEY"))
    candle_data = fetch_historical_data(client, "BTCUSDT", "1h", 1000)
    
    # init vars
    bt = BackTester(candle_data, 1000.0, 0.002)
    config = MovingAverageConfig(50, 200, "crossover")
    strat = MovingAverage(config)
    
    # run and print
    bt.run(strat)
    bt.print_results()
    


