import unittest
from test_data import make_client, RAW_TRADE, RAW_AGG_TRADE

from exceptions import FetchError
from data_structs import Trade, AggregrateTrade
import api_methods as am


class TestGetTrades(unittest.TestCase):

    def test_returns_list_of_trade_objects(self):
        client = make_client()
        client.get_recent_trades.return_value = [RAW_TRADE, RAW_TRADE]
        result = am.get_trades(client, "BTCUSDT", 2)
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], Trade)

    def test_trade_fields_parsed_correctly(self):
        client = make_client()
        client.get_recent_trades.return_value = [RAW_TRADE]
        trade = am.get_trades(client, "BTCUSDT", 1)[0]
        self.assertEqual(trade.id, 123)
        self.assertEqual(trade.price, "50000.00")
        self.assertEqual(trade.quantity, "0.001")
        self.assertEqual(trade.is_buyer_maker, False)
        self.assertEqual(trade.is_best_match, True)

    def test_raises_fetch_error_on_failure(self):
        client = make_client()
        client.get_recent_trades.side_effect = Exception("error")
        with self.assertRaises(FetchError):
            am.get_trades(client, "BTCUSDT", 10)


class TestGetHistoricalTrades(unittest.TestCase):

    def test_returns_list_of_trade_objects(self):
        client = make_client()
        client.get_historical_trades.return_value = [RAW_TRADE, RAW_TRADE]
        result = am.get_historical_trades(client, "BTCUSDT", 2)
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], Trade)

    def test_defaults_from_id_to_none(self):
        client = make_client()
        client.get_historical_trades.return_value = []
        am.get_historical_trades(client, "BTCUSDT", 5)
        client.get_historical_trades.assert_called_once_with(symbol="BTCUSDT", limit=5, fromId=None)

    def test_passes_from_id_when_provided(self):
        client = make_client()
        client.get_historical_trades.return_value = []
        am.get_historical_trades(client, "BTCUSDT", 5, fromId=999)
        client.get_historical_trades.assert_called_once_with(symbol="BTCUSDT", limit=5, fromId=999)

    def test_raises_fetch_error_on_failure(self):
        client = make_client()
        client.get_historical_trades.side_effect = Exception("error")
        with self.assertRaises(FetchError):
            am.get_historical_trades(client, "BTCUSDT", 10)


class TestGetAggregateTrades(unittest.TestCase):

    def test_returns_list_of_aggregate_trade_objects(self):
        client = make_client()
        client.get_aggregate_trades.return_value = [RAW_AGG_TRADE, RAW_AGG_TRADE]
        result = am.get_aggregate_trades(client, "BTCUSDT", 2, 1000000, 2000000)
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], AggregrateTrade)

    def test_aggregate_trade_fields_parsed_correctly(self):
        client = make_client()
        client.get_aggregate_trades.return_value = [RAW_AGG_TRADE]
        trade = am.get_aggregate_trades(client, "BTCUSDT", 1, 1000000, 2000000)[0]
        self.assertEqual(trade.id, 456)
        self.assertEqual(trade.price, "50100.00")
        self.assertEqual(trade.quantity, "0.002")
        self.assertEqual(trade.first_trade_id, 100)
        self.assertEqual(trade.last_trade_id, 105)
        self.assertEqual(trade.is_buyer_maker, True)

    def test_passes_correct_time_range(self):
        client = make_client()
        client.get_aggregate_trades.return_value = []
        am.get_aggregate_trades(client, "BTCUSDT", 5, 1000, 2000)
        client.get_aggregate_trades.assert_called_once_with(
            symbol="BTCUSDT", limit=5, startTime=1000, endTime=2000
        )

    def test_raises_fetch_error_on_failure(self):
        client = make_client()
        client.get_aggregate_trades.side_effect = Exception("error")
        with self.assertRaises(FetchError):
            am.get_aggregate_trades(client, "BTCUSDT", 5, 1000, 2000)


if __name__ == "__main__":
    unittest.main(verbosity=2)