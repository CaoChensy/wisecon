import unittest
from pprint import pprint
from wisecon.stock.financial import *


class TestDividend(unittest.TestCase):

    def test_dividend(self):
        """"""
        data = StockDividend(date="2024-09-30", size=5).load()
        data.show_columns()
        print(data.to_frame(chinese_column=True).to_markdown())

    def test_stock(self):
        data = StockDividend(start_date="2022-01-31", security_code="601899", size=5).load()
        print(data.to_frame(chinese_column=True).to_markdown())


class TestStockBalance(unittest.TestCase):
    """"""
    def test_balance(self):
        """"""
        data = StockBalance(date="2024-09-30", size=5).load()
        # pprint(data.to_dict(chinese_column=True)[0], indent=4)
        data.show_columns()
        print(data.to_frame(chinese_column=True).to_markdown())

    def test_industry(self):
        """"""
        data = StockBalance(start_date="2024-01-31", size=5, industry_name="纺织服装").load()
        print(data.to_frame(chinese_column=True).to_markdown())

    def test_stock(self):
        data = StockBalance(start_date="2024-01-31", size=5, security_code="603889").load()
        print(data.to_frame(chinese_column=True).to_markdown())


class TestEarnForcast(unittest.TestCase):
    def test_columns(self):
        data = EarnForcast(date="2024-09-30", size=5).load()
        # pprint(data.to_dict(chinese_column=True)[0], indent=4)
        data.show_columns()
        print(data.to_frame(chinese_column=True).to_markdown())

    def test_stock(self):
        """"""
        data = EarnForcast(date="2024-09-30", security_code="301626", size=5).load()
        print(data.to_frame(chinese_column=True).to_markdown())


class TestEarn(unittest.TestCase):
    def test_columns(self):
        data = Earn(date="2024-09-30", size=5).load()
        # pprint(data.to_dict(chinese_column=True)[0], indent=4)
        data.show_columns()
        print(data.to_frame(chinese_column=True).to_markdown())

    def test_stock(self):
        """"""
        data = Earn(date="2024-09-30", security_code="603889", size=5).load()
        print(data.to_frame(chinese_column=True).to_markdown())


class TestFastEarn(unittest.TestCase):
    def test_columns(self):
        data = EarnFast(date="2024-09-30", size=5).load()
        # pprint(data.to_dict(chinese_column=True)[0], indent=4)
        data.show_columns()
        print(data.to_frame(chinese_column=True).to_markdown())

    def test_stock(self):
        """"""
        data = EarnFast(date="2024-09-30", security_code="600995", size=5).load()
        print(data.to_frame(chinese_column=True).to_markdown())


class TestScheduledDisclosure(unittest.TestCase):
    def test_columns(self):
        data = ScheduledDisclosure(date="2024-09-30", size=5).load()
        # pprint(data.to_dict(chinese_column=True)[0], indent=4)
        data.show_columns()
        print(data.to_frame(chinese_column=True).to_markdown())

    def test_stock(self):
        """"""
        data = ScheduledDisclosure(date="2024-09-30", security_code="600816", size=5).load()
        print(data.to_frame(chinese_column=True).to_markdown())


class TestStockIncome(unittest.TestCase):
    def test_columns(self):
        data = StockIncome(date="2024-09-30", size=5).load()
        # pprint(data.to_dict(chinese_column=True)[0], indent=4)
        data.show_columns()
        print(data.to_frame(chinese_column=True).to_markdown())

    def test_stock(self):
        """"""
        data = StockIncome(date="2024-09-30", security_code="600816", size=5).load()
        print(data.to_frame(chinese_column=True).to_markdown())


class TestStockCashFlow(unittest.TestCase):
    def test_columns(self):
        data = StockCashFlow(date="2024-09-30", size=5).load()
        pprint(data.to_dict(chinese_column=True)[0], indent=4)
        data.show_columns()
        print(data.to_frame(chinese_column=True).to_markdown())

    def test_stock(self):
        """"""
        data = StockCashFlow(date="2024-09-30", security_code="600816", size=5).load()
        print(data.to_frame(chinese_column=True).to_markdown())
