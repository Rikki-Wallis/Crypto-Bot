import os
from api_methods import fetch_historical_data, get_market_depth

# API imports
from binance.client import Client
from dotenv import load_dotenv

if __name__ == "__main__":
    
    # Create api client
    load_dotenv()
    client = Client(os.getenv("BINANCE_API_KEY"), os.getenv("BINANCE_SECRET_KEY"), testnet=True)
    
    # Fetch history
    history = fetch_historical_data(client, symbol="BTCUSDT", interval="1h", limit=10)
    
    # Fetch market depth
    market_depth = get_market_depth(client, symbol="BTCUSDT", limit=10)
    
    for candle in history:
        print(str(candle))
        
    print(str(market_depth))
    
    