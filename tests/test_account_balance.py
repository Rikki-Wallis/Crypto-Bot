import unittest
import sys

from test_data import make_client

from exceptions import FetchError, BalanceError
import api_methods as am


class TestGetBalance(unittest.TestCase):

    def test_returns_free_balance_as_float(self):
        client = make_client()
        client.get_asset_balance.return_value = {"asset": "USDT", "free": "500.75", "locked": "100.00"}
        result = am.get_balance(client, "USDT")
        self.assertIsInstance(result, float)
        self.assertAlmostEqual(result, 500.75)

    def test_does_not_return_locked_balance(self):
        client = make_client()
        client.get_asset_balance.return_value = {"asset": "USDT", "free": "500.75", "locked": "100.00"}
        result = am.get_balance(client, "USDT")
        self.assertNotAlmostEqual(result, 100.00)

    def test_raises_balance_error_on_failure(self):
        client = make_client()
        client.get_asset_balance.side_effect = Exception("auth error")
        with self.assertRaises(BalanceError):
            am.get_balance(client, "USDT")


class TestGetAllBalances(unittest.TestCase):

    def test_returns_only_non_zero_balances(self):
        client = make_client()
        client.get_account.return_value = {
            "balances": [
                {"asset": "BTC",  "free": "0.5",   "locked": "0.0"},
                {"asset": "ETH",  "free": "0.0",   "locked": "0.0"},   # zero - excluded
                {"asset": "USDT", "free": "100.0", "locked": "50.0"},
            ]
        }
        result = am.get_all_balances(client)
        assets = [b["asset"] for b in result]
        self.assertIn("BTC", assets)
        self.assertIn("USDT", assets)
        self.assertNotIn("ETH", assets)

    def test_includes_assets_with_only_locked_balance(self):
        client = make_client()
        client.get_account.return_value = {
            "balances": [
                {"asset": "BNB", "free": "0.0", "locked": "5.0"},
            ]
        }
        result = am.get_all_balances(client)
        self.assertEqual(result[0]["asset"], "BNB")

    def test_raises_balance_error_on_failure(self):
        client = make_client()
        client.get_account.side_effect = Exception("auth error")
        with self.assertRaises(BalanceError):
            am.get_all_balances(client)


class TestGetTradeFee(unittest.TestCase):

    def test_returns_fee_info(self):
        client = make_client()
        client.get_trade_fee.return_value = [{"symbol": "BTCUSDT", "makerCommission": "0.001", "takerCommission": "0.001"}]
        result = am.get_trade_fee(client, "BTCUSDT")
        client.get_trade_fee.assert_called_once_with(symbol="BTCUSDT")
        self.assertEqual(result[0]["makerCommission"], "0.001")

    def test_raises_fetch_error_on_failure(self):
        client = make_client()
        client.get_trade_fee.side_effect = Exception("error")
        with self.assertRaises(FetchError):
            am.get_trade_fee(client, "BTCUSDT")


if __name__ == "__main__":
    unittest.main(verbosity=2)