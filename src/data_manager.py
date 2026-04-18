from exceptions import BuyError, FetchError, CancelError, BalanceError, OrderStatusError
from data_structs import ImportFix, Candle, MarketDepth, Trade, AggregrateTrade


# --- Price & Market Data ---
def get_current_price(client, symbol):
    try:
        return client.get_symbol_ticker(symbol=symbol)
    except:
        raise FetchError("Failed to fetch current price")

def get_avg_price(client, symbol):
    """
    5-minute average price.
    """
    try:
        return client.get_avg_price(symbol=symbol)
    except:
        raise FetchError("Failed to fetch average price")

def get_24h_stats(client, symbol):
    """
    Price change %, volume, high/low over the last 24 hours
    """
    try:
        return client.get_ticker(symbol=symbol)
    except:
        raise FetchError("Failed to fetch 24h stats")

def fetch_historical_data(client, symbol, interval, limit):
    try:
        klines = client.get_klines(symbol=symbol, interval=interval, limit=limit)
    except:
        raise FetchError("Failed to fetch history")

    candles = []
    for k in klines:
        candles.append(Candle(k))

    return candles


# --- Order Book & Depth ---
def get_market_depth(client, symbol, limit):
    try:
        order_book = client.get_order_book(symbol=symbol, limit=limit)
    except:
        raise FetchError("Failed to fetch market depth")

    return MarketDepth(order_book)


# --- Trade History ---
def get_trades(client, symbol, limit):
    try:
        recent_trades = client.get_recent_trades(symbol=symbol, limit=limit)
    except:
        raise FetchError("Failed to fetch recent trades")

    trades = []
    for trade in recent_trades:
        trades.append(Trade(trade))

    return trades

def get_historical_trades(client, symbol, limit, fromId=None):
    try:
        history_trades = client.get_historical_trades(symbol=symbol, limit=limit, fromId=fromId)
    except:
        raise FetchError("Failed to fetch history trades")

    trades = []
    for trade in history_trades:
        trades.append(Trade(trade))

    return trades

def get_aggregate_trades(client, symbol, limit, start_time, end_time):
    try:
        aggregate_trades = client.get_aggregate_trades(
            symbol=symbol, limit=limit, startTime=start_time, endTime=end_time
        )
    except:
        raise FetchError("Failed to fetch aggregate trades")

    trades = []
    for trade in aggregate_trades:
        trades.append(AggregrateTrade(trade))

    return trades


# --- Order Placement ---
def make_order(client, symbol, quantity):
    """
    Market buy at current best price.
    """
    try:
        return client.order_market_buy(symbol=symbol, quantity=quantity)
    except:
        raise BuyError("Failed to buy")

def make_sell_order(client, symbol, quantity):
    """
    Market sell at current best price.
    """
    try:
        return client.order_market_sell(symbol=symbol, quantity=quantity)
    except:
        raise BuyError("Failed to sell")

def make_limit_buy(client, symbol, quantity, price):
    """
    Limit buy, only fills at the specified price or better.
    """
    try:
        return client.order_limit_buy(symbol=symbol, quantity=quantity, price=price)
    except:
        raise BuyError("Failed to place limit buy")

def make_limit_sell(client, symbol, quantity, price):
    """
    Limit sell, only fills at the specified price or better.
    """
    try:
        return client.order_limit_sell(symbol=symbol, quantity=quantity, price=price)
    except:
        raise BuyError("Failed to place limit sell")

def make_stop_loss(client, symbol, quantity, stop_price):
    """
    Stop-loss limit sell. Triggers a limit sell when price hits stop_price.
    Always attach after opening a position
    """
    try:
        return client.create_order(
            symbol=symbol,
            side="SELL",
            type="STOP_LOSS_LIMIT",
            timeInForce="GTC",
            quantity=quantity,
            stopPrice=stop_price,
            price=stop_price
        )
    except:
        raise BuyError("Failed to place stop loss")

def make_oco_sell(client, symbol, quantity, take_profit_price, stop_price):
    """
    One-Cancels-the-Other sell order. Places a take-profit and stop-loss
    simultaneously, whichever triggers first cancels the other.
    """
    try:
        return client.create_oco_order(
            symbol=symbol,
            side="SELL",
            quantity=quantity,
            price=take_profit_price,
            stopPrice=stop_price,
            stopLimitPrice=stop_price,
            stopLimitTimeInForce="GTC"
        )
    except:
        raise BuyError("Failed to place OCO sell")


# --- Order Management ---
def get_order_status(client, symbol, order_id):
    """
    Check whether an order is NEW, PARTIALLY_FILLED, FILLED, or CANCELED.
    """
    try:
        return client.get_order(symbol=symbol, orderId=order_id)
    except:
        raise OrderStatusError("Failed to fetch order status")

def get_open_orders(client, symbol):
    """
    Returns all unfilled/partially filled orders for a symbol.
    """
    try:
        return client.get_open_orders(symbol=symbol)
    except:
        raise FetchError("Failed to fetch open orders")

def cancel_order(client, symbol, order_id):
    """
    Cancel a pending limit or stop order that hasn't filled yet.
    """
    try:
        return client.cancel_order(symbol=symbol, orderId=order_id)
    except:
        raise CancelError("Failed to cancel order")

def cancel_all_open_orders(client, symbol):
    """
    Cancel every open order for a symbol, useful for emergency exits.
    """
    try:
        return client.cancel_open_orders(symbol=symbol)
    except:
        raise CancelError("Failed to cancel all open orders")


# --- Account & Balance ---
def get_balance(client, asset):
    """
    Returns available (free) balance for an asset e.g. get_balance(client, 'USDT').
    'free' = spendable, 'locked' = held in open orders.
    """
    try:
        balance = client.get_asset_balance(asset=asset)
        return float(balance["free"])
    except:
        raise BalanceError("Failed to fetch balance")

def get_all_balances(client):
    """
    Returns all non-zero asset balances on the account.
    """
    try:
        account = client.get_account()
        return [b for b in account["balances"] if float(b["free"]) > 0 or float(b["locked"]) > 0]
    except:
        raise BalanceError("Failed to fetch all balances")

def get_trade_fee(client, symbol):
    """
    Returns maker/taker fee for a symbol.
    Critical for accurate P&L calculations, fees eat into profit significantly.
    """
    try:
        return client.get_trade_fee(symbol=symbol)
    except:
        raise FetchError("Failed to fetch trade fee")


# --- Exchange Info & Utilities ---
def get_symbol_info(client, symbol):
    """
    Returns trading rules for a symbol: minQty, maxQty, stepSize, minNotional.
    Always call this before placing orders to avoid silent rejections from Binance.
    """
    try:
        return client.get_symbol_info(symbol=symbol)
    except:
        raise FetchError("Failed to fetch symbol info")

def get_exchange_info(client):
    """
    Returns all available trading pairs, their status, and rate limit rules.
    Useful for discovering valid symbols and understanding API constraints.
    """
    try:
        return client.get_exchange_info()
    except:
        raise FetchError("Failed to fetch exchange info")

def get_server_time(client):
    """
    Syncs your local timestamps with Binance server time.
    Timestamp mismatches cause request rejections, call this on startup.
    """
    try:
        return client.get_server_time()
    except:
        raise FetchError("Failed to fetch server time")



# --- WebSocket Streams ---
def start_price_stream(bsm, symbol, callback):
    """
    Real-time price stream via WebSocket. Far more efficient than polling
    get_current_price() in a loop, use this for live trading.

    Args:
        bsm: BinanceSocketManager instance
        symbol: e.g. 'BTCUSDT'
        callback: function that receives each price update message

    Example:
        def handle_price(msg):
            print(msg['c'])  # 'c' = current close/price

        bsm = BinanceSocketManager(client)
        start_price_stream(bsm, 'BTCUSDT', handle_price)
    """
    return bsm.start_symbol_ticker_socket(symbol=symbol, callback=callback)

def start_kline_stream(bsm, symbol, interval, callback):
    """
    Real-time candlestick stream via WebSocket. Delivers a new candle update
    on every tick within the interval, use this to drive live strategy logic.

    Args:
        bsm: BinanceSocketManager instance
        symbol: e.g. 'BTCUSDT'
        interval: e.g. Client.KLINE_INTERVAL_1MINUTE
        callback: function that receives each candle update message

    Example:
        def handle_candle(msg):
            candle = msg['k']
            print(candle['c'])  # current close price

        bsm = BinanceSocketManager(client)
        start_kline_stream(bsm, 'BTCUSDT', Client.KLINE_INTERVAL_1MINUTE, handle_candle)
    """
    return bsm.start_kline_socket(symbol=symbol, interval=interval, callback=callback)

def start_depth_stream(bsm, symbol, callback):
    """
    Real-time order book (depth) stream via WebSocket.
    Use this to track live bid/ask changes without hammering the REST API.
    """
    return bsm.start_depth_socket(symbol=symbol, callback=callback)

def stop_stream(bsm, conn_key):
    """
    Stop a specific WebSocket stream by its connection key.
    """
    bsm.stop_socket(conn_key)

def start_socket_manager(bsm):
    """
    Start the Twisted reactor loop that powers all WebSocket streams.
    """
    bsm.start()