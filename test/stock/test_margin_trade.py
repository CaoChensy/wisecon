import unittest
from wisecon.stock.margin import *


class TestMarginTradeSummary(unittest.TestCase):
    """"""

    def test_margin_trade_summary(self):
        """"""
        data = MarginTradingSummary().load()
        print(data.to_frame(chinese_column=True).to_markdown())

    def test_margin_trade_summary_sh(self):
        """"""
        data = MarginTradingSummary(market="沪市").load()
        print(data.to_frame(chinese_column=True).to_markdown())

    def test_margin_trade_summary_sz(self):
        """"""
        data = MarginTradingSummary(market="深市").load()
        print(data.to_frame(chinese_column=True).to_markdown())

    def test_margin_trade_summary_js(self):
        """"""
        data = MarginTradingSummary(market="京市").load()
        print(data.to_frame(chinese_column=True).to_markdown())

    def test_margin_trade_summary_date(self):
        """"""
        data = MarginTradingSummary(market="京市", start_date="2024-10-10").load()
        print(data.to_frame(chinese_column=True).to_markdown())


class TestMarginTradeAccount(unittest.TestCase):
    """"""
    def test_margin_trade_account_day(self):
        """"""
        data = MarginTradingAccount(cycle="day").load()
        print(data.to_frame(chinese_column=True).to_markdown())

    def test_margin_trade_account_month(self):
        """"""
        data = MarginTradingAccount(cycle="month").load()
        print(data.to_frame(chinese_column=True).to_markdown())


class TestMarginTradePlate(unittest.TestCase):
    """"""
    def test_margin_trade_plate_industry(self):
        """"""
        data = MarginTradingPlate(plate_name="行业", cycle=1).load()
        print(data.to_frame(chinese_column=True).to_markdown())

    def test_margin_trade_plate_conception(self):
        """"""
        data = MarginTradingPlate(plate_name="概念", cycle=1).load()
        print(data.to_frame(chinese_column=True).to_markdown())

    def test_margin_trade_plate_zone(self):
        """"""
        data = MarginTradingPlate(plate_name="地域", cycle=1).load()
        print(data.to_frame(chinese_column=True).to_markdown())

    def test_margin_trade_plate_zone_3day(self):
        """"""
        data = MarginTradingPlate(plate_name="地域", cycle=3, verbose=True).load()
        print(data.to_frame(chinese_column=True).to_markdown())

    def test_margin_trade_plate_zone_5day(self):
        """"""
        data = MarginTradingPlate(plate_name="地域", cycle=5, verbose=True).load()
        print(data.to_frame(chinese_column=True).to_markdown())

    def test_margin_trade_plate_zone_date(self):
        """"""
        data = MarginTradingPlate(plate_name="地域", cycle=5, date="2024-10-10").load()
        print(data.to_frame(chinese_column=True).to_markdown())


class TestMarginTradeStock(unittest.TestCase):
    """
    融资融券交易明细:
        个股融资融券
    """
    def test_margin_trade_stock_total(self):
        """"""
        data = MarginTradingStock(date="2024-10-30", cycle=1, verbose=True).load()
        print(data.to_frame(chinese_column=True).to_markdown())

    def test_margin_trade_stock_HSA(self):
        """"""
        data = MarginTradingStock(market="沪深A股", date="2024-10-30", cycle=1, verbose=True).load()
        print(data.to_frame(chinese_column=True).to_markdown())

    def test_margin_trade_stock_KC(self):
        """"""
        data = MarginTradingStock(market="科创板", date="2024-10-30", cycle=1, verbose=True).load()
        print(data.to_frame(chinese_column=True).to_markdown())


class TestDailyMarginTrade(unittest.TestCase):
    """
    融资融券交易明细:
        日融资融券交易明细
    """

    def test_margin_trade_daily(self):
        """"""
        data = MarginTradingDaily().load()
        print(data.to_markdown(chinese_column=True))
