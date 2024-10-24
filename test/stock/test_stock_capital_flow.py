import unittest
from wisecon.stock.capital_flow import *


class TestStockFlow(unittest.TestCase):

    def test_moke(self):
        """"""
        data = StockFlow(days=1).load()
        data.show_columns()
        print(data.to_frame().to_markdown())
        print(data.to_frame(chinese_column=True).to_markdown())


class TestPlateFlow(unittest.TestCase):

    def test_moke(self):
        """"""
        data = PlateFlow(days=1).load()
        data.show_columns()
        print(data.to_frame().to_markdown())
        print(data.to_frame(chinese_column=True).to_markdown())
