import unittest
from unittest.mock import MagicMock
from test_data import make_bsm

import api_methods as am


class TestStartPriceStream(unittest.TestCase):

    def test_calls_start_symbol_ticker_socket_and_returns_key(self):
        bsm = make_bsm()
        callback = MagicMock()
        bsm.start_symbol_ticker_socket.return_value = "conn_key_1"
        result = am.start_price_stream(bsm, "BTCUSDT", callback)
        bsm.start_symbol_ticker_socket.assert_called_once_with(symbol="BTCUSDT", callback=callback)
        self.assertEqual(result, "conn_key_1")


class TestStartKlineStream(unittest.TestCase):

    def test_calls_start_kline_socket_and_returns_key(self):
        bsm = make_bsm()
        callback = MagicMock()
        bsm.start_kline_socket.return_value = "conn_key_2"
        result = am.start_kline_stream(bsm, "BTCUSDT", "1m", callback)
        bsm.start_kline_socket.assert_called_once_with(symbol="BTCUSDT", interval="1m", callback=callback)
        self.assertEqual(result, "conn_key_2")


class TestStartDepthStream(unittest.TestCase):

    def test_calls_start_depth_socket_and_returns_key(self):
        bsm = make_bsm()
        callback = MagicMock()
        bsm.start_depth_socket.return_value = "conn_key_3"
        result = am.start_depth_stream(bsm, "BTCUSDT", callback)
        bsm.start_depth_socket.assert_called_once_with(symbol="BTCUSDT", callback=callback)
        self.assertEqual(result, "conn_key_3")


class TestStopStream(unittest.TestCase):

    def test_calls_stop_socket_with_conn_key(self):
        bsm = make_bsm()
        am.stop_stream(bsm, "conn_key_1")
        bsm.stop_socket.assert_called_once_with("conn_key_1")


class TestStartSocketManager(unittest.TestCase):

    def test_calls_bsm_start(self):
        bsm = make_bsm()
        am.start_socket_manager(bsm)
        bsm.start.assert_called_once()


if __name__ == "__main__":
    unittest.main(verbosity=2)