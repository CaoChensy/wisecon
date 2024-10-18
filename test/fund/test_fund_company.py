import unittest
from wisecon.fund.fund_company import FundCompany


class TestFundList(unittest.TestCase):
    def test_fund_hist(self):
        """"""
        data = FundCompany(verbose=True).load()
        data.pprint_metadata()
        print(data.to_frame().head().to_markdown())
        print(data.to_frame(chinese_column=True).head().to_markdown())
