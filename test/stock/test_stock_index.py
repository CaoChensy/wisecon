import unittest
from pprint import pprint
from wisecon.stock.index import *


class TestHolderStockAnalysis(unittest.TestCase):

    def test_columns(self):
        """"""
        data = IndexStock(size=5, verbose=True).load()
        pprint(data.to_dict(chinese_column=True)[0], indent=4)

    def test_load(self):
        """
        :return:
        """
        data = IndexStock(size=5, verbose=True).load()
        data.show_columns()
        print(data.to_frame(chinese_column=True).to_markdown())

    def test_stock(self):
        """
        :return:
        """
        for index_name in ["沪深300", "上证50", "中证500", "科创50"]:
            print(index_name)
            data = IndexStock(index_name=index_name, size=5).load()
            print(data.to_frame(chinese_column=True).to_markdown())
            print("=" * 100)
