import unittest
from test_data import make_client, RAW_KLINE

from exceptions import FetchError
from data_structs import Candle
import api_methods as am


class TestGetCurrentPrice(unittest.TestCase):
    def test_returns_ticker(self):
        client = make_client()
        client.get_symbol_ticker.return_value = {"symbol": "BTCUSDT", "price": "50000.00"}
        result = am.get_current_price(client, "BTCUSDT")
        client.get_symbol_ticker.assert_called_once_with(symbol="BTCUSDT")
        self.assertEqual(result["price"], "50000.00")

    def test_raises_fetch_error_on_failure(self):
        client = make_client()
        client.get_symbol_ticker.side_effect = Exception("API down")
        with self.assertRaises(FetchError):
            am.get_current_price(client, "BTCUSDT")


class TestGetAvgPrice(unittest.TestCase):

    def test_returns_avg_price(self):
        client = make_client()
        client.get_avg_price.return_value = {"mins": 5, "price": "49800.00"}
        result = am.get_avg_price(client, "BTCUSDT")
        client.get_avg_price.assert_called_once_with(symbol="BTCUSDT")
        self.assertEqual(result["mins"], 5)

    def test_raises_fetch_error_on_failure(self):
        client = make_client()
        client.get_avg_price.side_effect = Exception("timeout")
        with self.assertRaises(FetchError):
            am.get_avg_price(client, "BTCUSDT")


class TestGet24hStats(unittest.TestCase):

    def test_returns_ticker_stats(self):
        client = make_client()
        client.get_ticker.return_value = {"priceChangePercent": "2.5", "volume": "1200"}
        result = am.get_24h_stats(client, "BTCUSDT")
        client.get_ticker.assert_called_once_with(symbol="BTCUSDT")
        self.assertEqual(result["priceChangePercent"], "2.5")

    def test_raises_fetch_error_on_failure(self):
        client = make_client()
        client.get_ticker.side_effect = Exception("error")
        with self.assertRaises(FetchError):
            am.get_24h_stats(client, "BTCUSDT")


class TestFetchHistoricalData(unittest.TestCase):

    def test_returns_list_of_candle_objects(self):
        client = make_client()
        client.get_klines.return_value = [RAW_KLINE, RAW_KLINE]
        result = am.fetch_historical_data(client, "BTCUSDT", "1h", 2)
        client.get_klines.assert_called_once_with(symbol="BTCUSDT", interval="1h", limit=2)
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], Candle)

    def test_candle_fields_parsed_correctly(self):
        client = make_client()
        client.get_klines.return_value = [RAW_KLINE]
        candle = am.fetch_historical_data(client, "BTCUSDT", "1h", 1)[0]
        self.assertAlmostEqual(candle.open, 49000.0)
        self.assertAlmostEqual(candle.high, 51000.0)
        self.assertAlmostEqual(candle.low, 48500.0)
        self.assertAlmostEqual(candle.close, 50000.0)
        self.assertAlmostEqual(candle.volume, 120.5)
        self.assertAlmostEqual(candle.num_trades, 850.0)

    def test_returns_empty_list_for_no_klines(self):
        client = make_client()
        client.get_klines.return_value = []
        self.assertEqual(am.fetch_historical_data(client, "BTCUSDT", "1h", 10), [])

    def test_raises_fetch_error_on_failure(self):
        client = make_client()
        client.get_klines.side_effect = Exception("bad request")
        with self.assertRaises(FetchError):
            am.fetch_historical_data(client, "BTCUSDT", "1h", 10)


if __name__ == "__main__":
    unittest.main(verbosity=2)