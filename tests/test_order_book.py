import unittest
from test_data import make_client, RAW_ORDER_BOOK

from exceptions import FetchError
from data_structs import MarketDepth
import api_methods as am


class TestGetMarketDepth(unittest.TestCase):

    def test_returns_market_depth_object(self):
        client = make_client()
        client.get_order_book.return_value = RAW_ORDER_BOOK
        result = am.get_market_depth(client, "BTCUSDT", 10)
        client.get_order_book.assert_called_once_with(symbol="BTCUSDT", limit=10)
        self.assertIsInstance(result, MarketDepth)

    def test_market_depth_fields_parsed_correctly(self):
        client = make_client()
        client.get_order_book.return_value = RAW_ORDER_BOOK
        result = am.get_market_depth(client, "BTCUSDT", 10)
        self.assertEqual(result.last_updated_id, 999)
        self.assertEqual(len(result.bids), 2)
        self.assertEqual(len(result.asks), 2)
        self.assertEqual(result.bids[0][0], "49900.00")

    def test_raises_fetch_error_on_failure(self):
        client = make_client()
        client.get_order_book.side_effect = Exception("network error")
        with self.assertRaises(FetchError):
            am.get_market_depth(client, "BTCUSDT", 10)


if __name__ == "__main__":
    unittest.main(verbosity=2)