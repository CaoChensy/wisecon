import unittest
from quant_tools.valuation import IndustryValuation
from quant_tools.utils import year2date


class TestIndustryValuation(unittest.TestCase):
    """"""
    def test_valuation_date(self):
        """"""
        data = IndustryValuation(date="2024-10-10", industry_code=None).load()
        data.show_columns()
        print(data.to_frame(chinese_column=True).to_markdown())

    def test_industry_code(self):
        """"""
        data = IndustryValuation(start_date="2018-01-01", end_date="2018-12-31", limit=356, industry_code="016017").load()
        data.show_columns()
        print(data.to_frame(chinese_column=True).to_markdown())

    def test_save_data(self):
        """"""
        data = IndustryValuation(date="2024-10-10", industry_code=None).load()
        data.show_columns()
        print(data.to_frame(chinese_column=True).to_markdown())
