import unittest
from wisecon.stock.main_holder import *


class TestFundHolder(unittest.TestCase):
    def test_fund_holder_list(self):
        data = FundHolderList(holder_code="007751", date="2024-09-30").load()
        print(data.to_frame(chinese_column=True).to_markdown())

    def test_fund_main_holder(self):
        """"""
        data = MainHolder(holder="基金", date="2024-09-30").load()
        print(data.to_frame(chinese_column=True).to_markdown())

    def test_stock_fund_holder_history(self):
        """"""
        data = StockFundHolderHistory(security_code="000001", date="2024-09-30").load()
        print(data.to_frame(chinese_column=True).to_markdown())

    def test_stock_holder(self):
        data = StockHolder(security_code="603350", holder="基金", date="2024-09-30").load()
        print(data.to_frame(chinese_column=True).to_markdown())

    def test_stock_holder_collect(self):
        data = StockHolderCollect(security_code="603350", date="2024-09-30").load()
        print(data.to_frame(chinese_column=True).to_markdown())
