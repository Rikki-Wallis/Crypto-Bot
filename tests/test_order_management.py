import unittest
from test_data import make_client

from exceptions import FetchError, CancelError, OrderStatusError
import api_methods as am


class TestGetOrderStatus(unittest.TestCase):

    def test_returns_order_details(self):
        client = make_client()
        client.get_order.return_value = {"orderId": 99, "status": "FILLED"}
        result = am.get_order_status(client, "BTCUSDT", 99)
        client.get_order.assert_called_once_with(symbol="BTCUSDT", orderId=99)
        self.assertEqual(result["status"], "FILLED")

    def test_raises_order_status_error_on_failure(self):
        client = make_client()
        client.get_order.side_effect = Exception("not found")
        with self.assertRaises(OrderStatusError):
            am.get_order_status(client, "BTCUSDT", 99)


class TestGetOpenOrders(unittest.TestCase):

    def test_returns_open_orders(self):
        client = make_client()
        client.get_open_orders.return_value = [{"orderId": 1}, {"orderId": 2}]
        result = am.get_open_orders(client, "BTCUSDT")
        self.assertEqual(len(result), 2)

    def test_returns_empty_list_when_no_open_orders(self):
        client = make_client()
        client.get_open_orders.return_value = []
        self.assertEqual(am.get_open_orders(client, "BTCUSDT"), [])

    def test_raises_fetch_error_on_failure(self):
        client = make_client()
        client.get_open_orders.side_effect = Exception("error")
        with self.assertRaises(FetchError):
            am.get_open_orders(client, "BTCUSDT")


class TestCancelOrder(unittest.TestCase):

    def test_cancels_order(self):
        client = make_client()
        client.cancel_order.return_value = {"orderId": 7, "status": "CANCELED"}
        result = am.cancel_order(client, "BTCUSDT", 7)
        client.cancel_order.assert_called_once_with(symbol="BTCUSDT", orderId=7)
        self.assertEqual(result["status"], "CANCELED")

    def test_raises_cancel_error_on_failure(self):
        client = make_client()
        client.cancel_order.side_effect = Exception("already filled")
        with self.assertRaises(CancelError):
            am.cancel_order(client, "BTCUSDT", 7)


class TestCancelAllOpenOrders(unittest.TestCase):

    def test_cancels_all_orders(self):
        client = make_client()
        client.cancel_open_orders.return_value = [{"orderId": 1}, {"orderId": 2}]
        result = am.cancel_all_open_orders(client, "BTCUSDT")
        client.cancel_open_orders.assert_called_once_with(symbol="BTCUSDT")
        self.assertEqual(len(result), 2)

    def test_raises_cancel_error_on_failure(self):
        client = make_client()
        client.cancel_open_orders.side_effect = Exception("error")
        with self.assertRaises(CancelError):
            am.cancel_all_open_orders(client, "BTCUSDT")


if __name__ == "__main__":
    unittest.main(verbosity=2)