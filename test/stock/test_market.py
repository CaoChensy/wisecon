import unittest
from wisecon.stock.market import *


class TestETFMarket(unittest.TestCase):
    """"""
    def test_etf_market(self):
        """"""
        data = CurrentMarket(market="ETF").load()
        print(data.to_frame(chinese_column=True).to_markdown())

    def test_lof_market(self):
        """"""
        data = CurrentMarket(market="LOF").load()
        print(data.to_frame(chinese_column=True).to_markdown())

    def test_close_market(self):
        """"""
        data = CurrentMarket(market="封闭基金").load()
        print(data.to_frame(chinese_column=True).to_markdown())

    def test_stock_market_total_a(self):
        """"""
        data = CurrentMarket(market="上证A股").load()
        print(data.to_frame(chinese_column=True).to_markdown())

    def test_stock_market_total_sh_a(self):
        """"""
        data = CurrentMarket(market="京市A股").load()
        print(data.to_frame(chinese_column=True).to_markdown())

    def test_stock_market_AB(self):
        """"""
        data = CurrentMarket(market="上证AB股比价").load()
        print(data.to_frame(chinese_column=True).to_markdown())


class TestLastDayMarketSummary(unittest.TestCase):
    """"""
    def test_last_day_market_summary(self):
        """"""
        data = LastDayMarketSummary().load()
        print(data.to_frame(chinese_column=True).to_markdown())

