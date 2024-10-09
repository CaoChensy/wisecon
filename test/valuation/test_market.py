import unittest
from quant_tools.valuation.market import MarketValuation


class TestMarketValuation(unittest.TestCase):
    """"""
    def test_market_valuation(self):
        """"""
        for market in ["000300", "000001", "000688", "399001", "399006",]:
            print(f"Market: {market}")
            market = MarketValuation(market=market, limit=5)
            data = market.load_data()
            data.pprint_metadata()
            print(data.to_frame(columns=data.metadata.get("columns")).to_markdown())

    def test_market_date(self):
        market = MarketValuation(market="000300", start_date="2018-12-01", end_date="2019-01-01", limit=5)
        data = market.load_data()
        data.pprint_metadata()
        print(data.to_frame(columns=data.metadata.get("columns")).to_markdown())
