import unittest
from wisecon.fund import FundBase


class TestFundBase(unittest.TestCase):
    def test_fund_list(self):
        data = FundBase(fund_code="000746").load()
        data.show_columns()
        print(data.to_frame().head().to_markdown())
        print(data.to_frame(chinese_column=True).head().to_markdown())

        