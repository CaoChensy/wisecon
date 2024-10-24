import unittest
from wisecon.fund import FundList


class TestFundList(unittest.TestCase):
    def test_fund_list(self):
        data = FundList().load()
        data.show_columns()
        print(data.to_frame().head().to_markdown())
        print(data.to_frame(chinese_column=True).tail().to_markdown())
