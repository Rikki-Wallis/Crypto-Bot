import sys
import os

sys.path.append('../src')

from unittest.mock import MagicMock

# Raw Binance API responses, data used across all test files
RAW_TRADE = {
    "id": 123,
    "price": "50000.00",
    "quantity": "0.001",
    "time": 1712345678000,
    "isBuyerMaker": False,
    "isBestMatch": True,
}

RAW_AGG_TRADE = {
    "a": 456,
    "p": "50100.00",
    "q": "0.002",
    "f": 100,
    "l": 105,
    "T": 1712345679000,
    "m": True,
    "M": True,
}

RAW_ORDER_BOOK = {
    "lastUpdateId": 999,
    "bids": [["49900.00", "1.5"], ["49800.00", "2.0"]],
    "asks": [["50100.00", "0.5"], ["50200.00", "1.0"]],
}

RAW_KLINE = [
    "1712300000000", "49000.0", "51000.0", "48500.0", "50000.0",
    "120.5", "1712303600000", "6025000.0", "850", "60.2", "3012500.0"
]


def make_client():
    return MagicMock()

def make_bsm():
    return MagicMock()