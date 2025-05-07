import unittest
from wisecon.stock.kline import *


class TestKLine(unittest.TestCase):

    def test_300(self):
        """"""
        data = KLine(market_code="000300", period="1D", size=5, verbose=True).load()
        print(data.to_markdown(chinese_column=True))

    def test_stock(self):
        """"""
        # data = KLine(security_code="300069", period="1D", size=5, verbose=True).load()
        # data = KLine(security_code="601939", period="1D", size=5, verbose=True).load()
        data = KLine(security_code="002006", period="1D", size=5, verbose=True).load()
        print(data.to_markdown(chinese_column=True))

    def test_plate(self):
        """"""
        data = KLine(plate_code="BK0887", period="1D", size=5, verbose=True).load()
        print(data.to_markdown(chinese_column=True))

    def test_loop_period(self):
        """"""
        for period in ["1m", "5m", "15m", "30m", "60m", "1D", "1W", "1M"]:
            data = KLine(security_code="300069", period=period, size=5).load()
            print(period, data.to_frame(chinese_column=True).shape)


class TestMinKLine(unittest.TestCase):
    def test_1min(self):
        """"""
        data = KlineMin(security_code="300069", n_days=1, verbose=True).load()
        print(data.to_markdown(chinese_column=True))

    def test_plate(self):
        """"""
        data = KlineMin(plate_code="BK0887", n_days=1, verbose=True).load()
        print(data.to_markdown(chinese_column=True))
