import unittest
from wisecon.stock.etf import *


class TestETFGold(unittest.TestCase):
    """"""
    def test_etf_gold_bai(self):
        """"""
        data = ETFGoldHistory(market="ETF白银").load()
        print(data.to_frame(chinese_column=True).to_markdown())

    def test_etf_gold(self):
        """"""
        data = ETFGoldHistory(market="ETF黄金", date="2024-10-25").load()
        print(data.to_frame(chinese_column=True).to_markdown())

    def test_etf_gold_date(self):
        """"""
        data = ETFGoldHistory(market="ETF黄金", start_date="2024-10-25").load()
        print(data.to_frame(chinese_column=True).to_markdown())
