import unittest
from quant_tools.etf.market import ETFMarket


class TestETFMarket(unittest.TestCase):
    """"""
    def test_etf_market(self):
        """"""
        data = ETFMarket(verbose=True).load()
        data.show_columns()
        print(data.to_frame(chinese_column=True).to_markdown())
