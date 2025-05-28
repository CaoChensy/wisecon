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


class TestTotal(unittest.TestCase):
    """"""

    def test_list_all_stock(self):
        """"""
        list_stock = ListALLStock(size=10, market="沪深京A股")
        print(list_stock.load().to_markdown(chinese_column=True))

    def test_list_all_stock_not_size(self):
        """"""
        list_stock = ListALLStock(market="沪深京A股")
        df_stock = list_stock.load().to_frame(chinese_column=True)
        print(len(df_stock), df_stock.drop_duplicates().shape[0])

