from constants import HOLD, BUY, SELL

class Strategy:
    def __init__(self, config):
        raise NotImplementedError
        
    def generate_signal(candles):
        raise NotImplementedError

"""
    Moving Average Strategy & Config
"""
class MovingAverageConfig:
    def __init__(self, short_window, long_window, signal_type):
        
        if short_window >= long_window:
            raise ValueError("Short window must be smaller than long window")
        
        self.short_window = short_window
        self.long_window = long_window
        self.signal_type = signal_type

class MovingAverage(Strategy):
    def __init__(self, config):
        self.config = config
        # crossover prevention
        self.previous_state = None
    
    def _moving_average(self, prices, window):
        if len(prices) < window:
            return None
        else:
            return sum(prices[-window:]) / window
    
    def generate_signal(self, candles):
        
        # Seperate closes
        closes = [candle.close for candle in candles]
        
        # Calculate moving avgs
        short_ma = self._moving_average(closes, self.config.short_window)
        long_ma = self._moving_average(closes, self.config.long_window)
        
        # Not enough data yet
        if short_ma is None or long_ma is None:
            return HOLD
        
        curr_state = short_ma > long_ma
        
        # Detect crossover
        if self.previous_state is None:
            self.previous_state = curr_state
            return HOLD
        
        if curr_state and not self.previous_state:
            self.previous_state = curr_state
            return BUY
        
        elif not curr_state and self.previous_state:
            self.previous_state = curr_state
            return SELL
        
        return HOLD
        