class ImportFix:
    def __init__(self):
        pass

class MarketDepth:
    def __init__(self, order_book):
        self.last_updated_id = order_book["lastUpdateId"]
        self.bids = order_book["bids"]
        self.asks = order_book["asks"]
        
    def __str__(self):
        out = f"\nLast Updated ID: {self.last_updated_id}"
        for i, bid in enumerate(self.bids):
            out += f"\nBid {i} \nPrice: {bid[0]} \nQuantity: {bid[1]}"
        
        for i, ask in enumerate(self.asks):
            out += f"\nAsk {i} Value: {ask}"
            
        return out
        

class Candle:
    def __init__(self, kline):
        self.open_time = float(kline[0])
        self.open = float(kline[1])
        self.high = float(kline[2])
        self.low = float(kline[3])
        self.close = float(kline[4])
        self.volume = float(kline[5])
        self.close_time = float(kline[6])
        self.quote_asset_volume = float(kline[7])
        self.num_trades = float(kline[8])
        self.taker_buy_base_asset_volume = float(kline[9])
        self.taker_buy_quote_asset_volume = float(kline[10])
    
    def __str__(self):
        return f"\nOpen Time: {self.open_time} \nOpen: {self.open} \nHigh: {self.high} \nLow: {self.low} \nClose: {self.close} \nVolume: {self.volume} \nClose Time: {self.close_time} \nQuote Asset Volume: {self.quote_asset_volume} \nNumber of Trades: {self.num_trades} \nTaker Buy Base Asset Volume: {self.taker_buy_base_asset_volume} \nTaker Buy Quote Asset Volume: {self.taker_buy_quote_asset_volume}"