import unittest
from quant_tools.fund.fund_hist import FundHist


class TestFundList(unittest.TestCase):
    def test_fund_hist(self):
        """"""
        fund_hist = FundHist(fund_code="000746")
        data = fund_hist.load_data()
        data.pprint_metadata()
        print(data.to_frame().head().to_markdown())
        print(data.to_frame(data.metadata.get("columns")).head().to_markdown())

    def test_fund_hist_date(self):
        """"""
        fund_hist = FundHist(fund_code="000746", start_date="2020-01-01", end_date="2024-01-01", limit=1000)
        data = fund_hist.load_data()
        print(data.to_frame().shape)
        print(data.to_frame().head().to_markdown())
