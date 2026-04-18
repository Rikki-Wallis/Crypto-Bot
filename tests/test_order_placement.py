import unittest
from test_data import make_client

from exceptions import BuyError
import api_methods as am


class TestMakeOrder(unittest.TestCase):

    def test_places_market_buy(self):
        client = make_client()
        client.order_market_buy.return_value = {"orderId": 1, "status": "FILLED"}
        result = am.make_order(client, "BTCUSDT", 0.001)
        client.order_market_buy.assert_called_once_with(symbol="BTCUSDT", quantity=0.001)
        self.assertEqual(result["status"], "FILLED")

    def test_raises_buy_error_on_failure(self):
        client = make_client()
        client.order_market_buy.side_effect = Exception("rejected")
        with self.assertRaises(BuyError):
            am.make_order(client, "BTCUSDT", 0.001)


class TestMakeSellOrder(unittest.TestCase):

    def test_places_market_sell(self):
        client = make_client()
        client.order_market_sell.return_value = {"orderId": 2, "status": "FILLED"}
        result = am.make_sell_order(client, "BTCUSDT", 0.001)
        client.order_market_sell.assert_called_once_with(symbol="BTCUSDT", quantity=0.001)
        self.assertEqual(result["status"], "FILLED")

    def test_raises_buy_error_on_failure(self):
        client = make_client()
        client.order_market_sell.side_effect = Exception("rejected")
        with self.assertRaises(BuyError):
            am.make_sell_order(client, "BTCUSDT", 0.001)


class TestMakeLimitBuy(unittest.TestCase):

    def test_places_limit_buy(self):
        client = make_client()
        client.order_limit_buy.return_value = {"orderId": 3, "status": "NEW"}
        result = am.make_limit_buy(client, "BTCUSDT", 0.001, "45000.00")
        client.order_limit_buy.assert_called_once_with(symbol="BTCUSDT", quantity=0.001, price="45000.00")
        self.assertEqual(result["status"], "NEW")

    def test_raises_buy_error_on_failure(self):
        client = make_client()
        client.order_limit_buy.side_effect = Exception("rejected")
        with self.assertRaises(BuyError):
            am.make_limit_buy(client, "BTCUSDT", 0.001, "45000.00")


class TestMakeLimitSell(unittest.TestCase):

    def test_places_limit_sell(self):
        client = make_client()
        client.order_limit_sell.return_value = {"orderId": 4, "status": "NEW"}
        result = am.make_limit_sell(client, "BTCUSDT", 0.001, "55000.00")
        client.order_limit_sell.assert_called_once_with(symbol="BTCUSDT", quantity=0.001, price="55000.00")
        self.assertEqual(result["status"], "NEW")

    def test_raises_buy_error_on_failure(self):
        client = make_client()
        client.order_limit_sell.side_effect = Exception("rejected")
        with self.assertRaises(BuyError):
            am.make_limit_sell(client, "BTCUSDT", 0.001, "55000.00")


class TestMakeStopLoss(unittest.TestCase):

    def test_places_stop_loss_order_with_correct_params(self):
        client = make_client()
        client.create_order.return_value = {"orderId": 5, "type": "STOP_LOSS_LIMIT"}
        result = am.make_stop_loss(client, "BTCUSDT", 0.001, "44000.00")
        client.create_order.assert_called_once_with(
            symbol="BTCUSDT",
            side="SELL",
            type="STOP_LOSS_LIMIT",
            timeInForce="GTC",
            quantity=0.001,
            stopPrice="44000.00",
            price="44000.00"
        )
        self.assertEqual(result["type"], "STOP_LOSS_LIMIT")

    def test_raises_buy_error_on_failure(self):
        client = make_client()
        client.create_order.side_effect = Exception("rejected")
        with self.assertRaises(BuyError):
            am.make_stop_loss(client, "BTCUSDT", 0.001, "44000.00")


class TestMakeOcoSell(unittest.TestCase):

    def test_places_oco_order_with_correct_params(self):
        client = make_client()
        client.create_oco_order.return_value = {"orderListId": 1}
        am.make_oco_sell(client, "BTCUSDT", 0.001, "56000.00", "44000.00")
        client.create_oco_order.assert_called_once_with(
            symbol="BTCUSDT",
            side="SELL",
            quantity=0.001,
            price="56000.00",
            stopPrice="44000.00",
            stopLimitPrice="44000.00",
            stopLimitTimeInForce="GTC"
        )

    def test_raises_buy_error_on_failure(self):
        client = make_client()
        client.create_oco_order.side_effect = Exception("rejected")
        with self.assertRaises(BuyError):
            am.make_oco_sell(client, "BTCUSDT", 0.001, "56000.00", "44000.00")


if __name__ == "__main__":
    unittest.main(verbosity=2)