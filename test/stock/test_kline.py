import unittest
from wisecon.stock.kline import KLine


class TestKLine(unittest.TestCase):

    def test_moke(self):
        """"""
        data = KLine(code="300069", end="20240910", period="1day", limit=9).load()
        data.show_columns()
        print(data.to_frame().to_markdown())
        print(data.to_frame(chinese_column=True).to_markdown())

    def test_KLine_period(self):
        """"""
        for period in ["1min", "5min", "15min", "30min", "60min", "1day", "1week", "1month"]:
            data = KLine(code="300069", period=period, limit=5).load()
            data.show_columns()
            print(data.to_frame(chinese_column=True).to_markdown())
