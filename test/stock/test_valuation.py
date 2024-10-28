import unittest
from wisecon.stock.valuation import *


class TestMarketValuation(unittest.TestCase):
    """"""
    def test_market_valuation(self):
        """"""
        data = MarketValuation(market="沪深两市", size=5).load()
        print(data.to_frame(chinese_column=True).to_markdown())

    def test_market_date(self):
        data = MarketValuation(market="沪深两市", start_date="2024-10-01", end_date="2024-10-20", size=50).load()
        print(data.to_frame(chinese_column=True).to_markdown())

    def test_market_valuation_loop(self):
        """"""
        for market in ["沪深两市", "沪市主板", "科创板", "深市主板", "创业板",]:
            print(f"Market: {market}")
            data = MarketValuation(market=market, size=5).load()
            print(data.to_frame(chinese_column=True).to_markdown())


class TestIndustryValuation(unittest.TestCase):
    """"""
    def test_valuation_date(self):
        """"""
        data = IndustryValuation(date="2024-10-10", verbose=True).load()
        print(data.to_frame(chinese_column=True).to_markdown())

    def test_industry_code(self):
        """"""
        data = IndustryValuation(start_date="2024-10-01", end_date="2024-10-20", limit=50, industry_code="016017").load()
        data.show_columns()
        print(data.to_frame(chinese_column=True).to_markdown())

    def test_save_data(self):
        """"""
        data = IndustryValuation(date="2024-10-10", industry_code=None).load()
        data.show_columns()
        print(data.to_frame(chinese_column=True).to_markdown())


class TestStockValuation(unittest.TestCase):
    """"""
    def test_valuation_date(self):
        """"""
        data = StockValuation(date="2024-09-30").load()
        print(data.to_frame(chinese_column=True).to_markdown())

    def test_industry_code(self):
        """"""
        data = StockValuation(date="2024-09-30", industry_code="016023").load()
        print(data.to_frame(chinese_column=True).to_markdown())

    def test_stock_code(self):
        """"""
        data = StockValuation(start_data="2024-08-30", code="000059").load()
        print(data.to_frame(chinese_column=True).to_markdown())
