import sqlite3
import unittest
from wisecon.update import UpdateKline


class TestUpdateKline(unittest.TestCase):
    """ Test UpdateKline class """

    def setUp(self):
        """"""
        self.conn = sqlite3.connect("/home/data/sqlite/kline.db")

    def test_update_kline(self):
        """"""
        update = UpdateKline(self.conn, verbose=True)
        update(security_code="000001")

    def test_kline(self):
        update = UpdateKline(self.conn, verbose=True)
        update(security_code="920819")

    def test_kline_market(self):
        update = UpdateKline(self.conn, verbose=True)
        update(market_code="000300")
