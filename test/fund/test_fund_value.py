import unittest
from wisecon.fund.fund_value import FundValue


class TestFundValue(unittest.TestCase):
    """ 测试：基金当前净值 """
    def test_fund_list(self):
        data = FundValue(fund_code="000001").load()
        data.show_columns()
        print(data.to_frame().shape)
        print(data.to_frame(chinese_column=True).head().to_markdown())

