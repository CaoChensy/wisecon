import unittest
from wisecon.mcp.report import *


class TestReportMapping(unittest.TestCase):
    """"""
    def test_report_mapping(self):
        """列出概念以及相关代码"""
        con_map = ConceptionMap()
        print(con_map.map_district)
        print(con_map.map_industry)
        print(con_map.map_conception)

    def test_get_name(self):
        """ 查询概念名称 """
        con_map = ConceptionMap()
        print(con_map.get_code_by_name(name="玻璃"))

    def test_get_code(self):
        """ 查询概念代码 """
        con_map = ConceptionMap()
        print(con_map.get_name_by_code(code="451"))
