import unittest
from wisecon.fund.fund_hist import FundHist


class TestFundList(unittest.TestCase):
    def test_fund_hist(self):
        """"""
        data = FundHist(fund_code="000746").load()
        print(data.to_frame().head().to_markdown())
        print(data.to_frame(data.metadata.get("columns")).head().to_markdown())

    def test_fund_hist_date(self):
        """"""
        data = FundHist(fund_code="000746", start_date="2020-01-01", end_date="2024-01-01", limit=10).load()
        print(data.to_frame().shape)
        print(data.to_frame(chinese_column=True).head().to_markdown())
