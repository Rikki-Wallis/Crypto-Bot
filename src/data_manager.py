from exceptions import BuyError, FetchError
from data_structs import ImportFix, Candle, MarketDepth


def make_order(client, symbol, quantity):
    try:
        return client.order_market_buy(symbol=symbol, quantity=quantity)
    except:
        raise BuyError("Failed to buy")
    
def get_current_price(client, symbol):
    try:
        return client.get_symbol_ticker(symbol=symbol)
    except:
        raise FetchError("Failed to fetch current price")

def fetch_historical_data(client, symbol, interval, limit):
    try:
        klines = client.get_klines(symbol=symbol, interval=interval, limit=limit)
    except:
        raise FetchError("Failed to fetch history")

    candles = []
    for k in klines:
        candles.append(Candle(k))
    
    return candles

def get_market_depth(client, symbol, limit):
    try:
        order_book = client.get_order_book(symbol=symbol, limit=limit)
        print(order_book)
    except:
        raise FetchError("Failed to fetch market depth")
    
    return MarketDepth(order_book)
