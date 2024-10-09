import unittest
from quant_tools.valuation import StockValuation


class TestStockValuation(unittest.TestCase):
    """"""
    def test_valuation_date(self):
        """"""
        market = StockValuation(date="2024-09-30", industry_code=None)
        data = market.load_data()
        data.pprint_metadata()
        print(data.to_frame(columns=data.metadata.get("columns")))

    def test_industry_code(self):
        """"""
        market = StockValuation(date="2024-09-30", industry_code="016023")
        data = market.load_data()
        data.pprint_metadata()
        print(data.to_frame(columns=data.metadata.get("columns")).to_markdown())

    def test_stock_code(self):
        """"""
        market = StockValuation(start_data="2024-08-30", code="000059")
        data = market.load_data()
        data.pprint_metadata()
        print(data.to_frame(columns=data.metadata.get("columns")).to_markdown())
