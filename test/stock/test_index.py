import unittest
from wisecon.stock.index import *


class TestSearch(unittest.TestCase):
    """"""
    def test_bk_1(self):
        search = SearchKeyword(keyword="华为")
        data = search.load()
        print(data.to_markdown())
        print(data.to_markdown(chinese_column=True))

    def test_bk_2(self):
        search = SearchKeyword(keyword="新能源", size=8)
        data = search.load()
        print(data.to_markdown())

    def test_bk_3(self):
        search = SearchKeyword(keyword="银行", size=5)
        data = search.load()
        print(data.to_markdown())


class TestListConceptionStock(unittest.TestCase):
    """"""

    def test_list_stock(self):
        """"""
        list_stock = ListConceptionStock(bk_code="BK0475", verbose=True)
        data = list_stock.load()
        print(data.to_markdown(chinese_column=True))

    def test_list_stock_2(self):
        """"""
        list_stock = ListConceptionStock(bk_code="BK0968", verbose=True)
        data = list_stock.load()
        print(data.to_markdown(chinese_column=True))

    def test_list_stock_3(self):
        """"""
        list_stock = ListConceptionStock(bk_code="BK1070", verbose=True)
        data = list_stock.load()
        print(data.to_markdown(chinese_column=True))


class TestReportMapping(unittest.TestCase):
    """"""
    def test_report_mapping(self):
        """列出概念以及相关代码"""
        con_map = ConceptionMap()
        print(con_map.map_district.to_markdown())
        print(con_map.map_industry.to_markdown())
        print(con_map.map_conception.to_markdown())

    def test_get_name(self):
        """ 查询概念名称 """
        con_map = ConceptionMap()
        print(con_map.get_code_by_name(name="玻璃"))
        print(con_map.get_code_by_name(name="华为"))
        print(con_map.get_code_by_name(name="快手"))

    def test_get_code(self):
        """ 查询概念代码 """
        con_map = ConceptionMap()
        print(con_map.get_name_by_code(code="451"))
