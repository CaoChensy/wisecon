import pprint
import unittest
from wisecon.stock.capital_flow import *


class TestStockFlow(unittest.TestCase):

    def test_columns(self):
        """"""
        data = StockFlow(days=1, size=10).load()
        pprint.pprint(data.to_dict(chinese_column=True)[0])
        print(data.metadata)

    def test_moke(self):
        """"""
        data = StockFlow(days=1).load()
        data.show_columns()
        print(data.to_frame().to_markdown())
        print(data.to_frame(chinese_column=True).to_markdown())


class TestPlateFlow(unittest.TestCase):

    def test_moke(self):
        """"""
        data = PlateFlow(days=1).load()
        data.show_columns()
        print(data.to_frame().to_markdown())
        print(data.to_frame(chinese_column=True).to_markdown())


class TestHistoryCapitalFlow(unittest.TestCase):

    def test_columns(self):
        """"""
        data = CapitalFlowHistory(market="沪B", verbose=True, size=10).load()
        pprint.pprint(data.to_dict(chinese_column=True)[-1])
        print(data.metadata)

    def test_market_history(self):
        """"""
        data = CapitalFlowHistory(market="沪深两市", verbose=True, size=10).load()
        print(data.to_frame().to_markdown())
        print(data.to_frame(chinese_column=True).to_markdown())

    def test_plate_history(self):
        """"""
        data = CapitalFlowHistory(plate_code="BK1044", verbose=True, size=10).load()
        print(data.metadata.response)
        print(data.to_frame(chinese_column=True).to_markdown())

    def test_security_code(self):
        """"""
        data = CapitalFlowHistory(security_code="300750", size=10).load()
        print(data.metadata.response)
        print(data.to_frame(chinese_column=True).to_markdown())


class TestCurrentCapitalFlow(unittest.TestCase):
    """"""
    def test_columns(self):
        """"""
        data = CapitalFlowCurrent(security_code=["601012", "300750"], verbose=True, size=10).load()
        pprint.pprint(data.to_dict(chinese_column=True)[-1])
        print(data.metadata)
        print(data.to_frame(chinese_column=True).to_markdown())
