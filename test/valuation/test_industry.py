import unittest
from quant_tools.valuation import IndustryValuation


class TestIndustryValuation(unittest.TestCase):
    """"""
    def test_valuation_date(self):
        """"""
        market = IndustryValuation(date="2024-09-30", industry_code=None)
        data = market.load_data()
        data.pprint_metadata()
        print(data.to_frame(columns=data.metadata.get("columns")).to_markdown())

    def test_industry_code(self):
        """"""
        market = IndustryValuation(start_date="2024-08-30", industry_code="016023")
        data = market.load_data()
        data.pprint_metadata()
        print(data.to_frame(columns=data.metadata.get("columns")).to_markdown())
