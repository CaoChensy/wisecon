import unittest
from wisecon.fund import *


class TestFundTrend(unittest.TestCase):
    def test_fund_trend(self):
        for period in ["1m", "3m", "6m", "1y", "3y", "5y", "this_year", "all"]:
            data = FundTrend(fund_code="000001", period=period).load()
            # data.pprint_metadata()
            print(f"{period} - {data.to_frame().shape}")
            print(data.to_frame(chinese_column=True).head().to_markdown())

    def test_fund_trend_all(self):
        data = FundTrend(fund_code="000001", period="all").load()
        data.pprint_metadata()
        print(data.to_frame(chinese_column=True))


class TestFundRant(unittest.TestCase):
    def test_fund_rant(self):
        """"""
        for period in ["1m", "3m", "6m", "1y", "3y", "5y", "this_year", "all"]:
            fund_trend = FundRant(fund_code="000746", period=period)
            data = fund_trend.load_data()
            # data.pprint_metadata()
            print(f"{period} - {data.to_frame().shape}")
            print(data.to_frame())

    def test_fund_rant_percent(self):
        """"""
        for period in ["1m", "3m", "6m", "1y", "3y", "5y", "this_year", "all"]:
            fund_trend = FundRant(fund_code="000746", percent=True, period=period)
            data = fund_trend.load_data()
            # data.pprint_metadata()
            print(f"{period} - {data.to_frame().shape}")
            print(data.to_frame())



