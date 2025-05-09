import unittest
from wisecon.mcp.report import *


class TestMCPReport(unittest.TestCase):
    """"""
    def test_get_now_date(self):
        """"""
        print(get_now_date())

    def test_get_industry_name_by_code(self):
        """"""
        data = get_industry_name_by_code(code="451")
        print(data)

    def test_get_industry_code_by_name(self):
        """"""
        data = get_industry_code_by_name("玻璃")
        print(data)

    def test_list_industry(self):
        """"""
        data = list_industry()
        print(data)

    def test_list_report(self):
        """"""
        data = list_report(report_type="行业研报", industry_code="451")
        print(data)

    def test_list_report_729(self):
        """"""
        data = list_report(report_type="行业研报", industry_code=729)
        print(data)

    def test_fetch_report_text(self):
        """"""
        data = fetch_report_text_by_code(**{"info_code": "AP202505081669269070"})
        data = fetch_report_text_by_code(**{"info_code": "AP202505081669269070"})
        print(data)

    def test_fetch_report_text_by_code_error(self):
        data = fetch_report_text_by_code(info_code="-asd919")
        print(data)
