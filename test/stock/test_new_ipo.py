import unittest
from wisecon.stock.new_ipo import *


class TestNewIPO(unittest.TestCase):

    def test_new_ipo_stock_all(self):
        data = NewIPOList(market="全部股票", verbose=True).load()
        print(data.to_frame(chinese_column=True).to_markdown())

    def test_new_ipo_stock_sh(self):
        data = NewIPOList(market="沪市主板", verbose=True).load()
        print(data.to_frame(chinese_column=True).to_markdown())

    def test_new_ipo_stock_kc(self):
        data = NewIPOList(market="科创板", verbose=True).load()
        print(data.to_frame(chinese_column=True).to_markdown())

    def test_new_ipo_stock_sz(self):
        data = NewIPOList(market="深市主板", verbose=True).load()
        print(data.to_frame(chinese_column=True).to_markdown())

    def test_new_ipo_stock_cy(self):
        data = NewIPOList(market="创业板", verbose=True).load()
        print(data.to_frame(chinese_column=True).to_markdown())

    def test_new_ipo_stock_bj(self):
        data = NewIPOList(market="北交所", verbose=True).load()
        print(data.to_frame(chinese_column=True).to_markdown())

    def test_new_ipo_stock_zai(self):
        data = NewIPOList(market="可转债", verbose=True).load()
        print(data.to_frame(chinese_column=True).to_markdown())

    def test_new_ipo_stock_reit(self):
        data = NewIPOList(market="REITs", verbose=True).load()
        print(data.to_frame(chinese_column=True).to_markdown())
