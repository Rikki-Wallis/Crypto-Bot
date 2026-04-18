import unittest
from test_data import make_client

from exceptions import FetchError
import api_methods as am


class TestGetSymbolInfo(unittest.TestCase):

    def test_returns_symbol_info(self):
        client = make_client()
        client.get_symbol_info.return_value = {"symbol": "BTCUSDT", "status": "TRADING"}
        result = am.get_symbol_info(client, "BTCUSDT")
        client.get_symbol_info.assert_called_once_with(symbol="BTCUSDT")
        self.assertEqual(result["status"], "TRADING")

    def test_raises_fetch_error_on_failure(self):
        client = make_client()
        client.get_symbol_info.side_effect = Exception("error")
        with self.assertRaises(FetchError):
            am.get_symbol_info(client, "BTCUSDT")


class TestGetExchangeInfo(unittest.TestCase):

    def test_returns_exchange_info(self):
        client = make_client()
        client.get_exchange_info.return_value = {"timezone": "UTC", "symbols": []}
        result = am.get_exchange_info(client)
        client.get_exchange_info.assert_called_once()
        self.assertIn("symbols", result)

    def test_raises_fetch_error_on_failure(self):
        client = make_client()
        client.get_exchange_info.side_effect = Exception("error")
        with self.assertRaises(FetchError):
            am.get_exchange_info(client)


class TestGetServerTime(unittest.TestCase):

    def test_returns_server_time(self):
        client = make_client()
        client.get_server_time.return_value = {"serverTime": 1712345678000}
        result = am.get_server_time(client)
        self.assertEqual(result["serverTime"], 1712345678000)

    def test_raises_fetch_error_on_failure(self):
        client = make_client()
        client.get_server_time.side_effect = Exception("error")
        with self.assertRaises(FetchError):
            am.get_server_time(client)


if __name__ == "__main__":
    unittest.main(verbosity=2)