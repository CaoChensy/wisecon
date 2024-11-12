import pprint
import unittest
from wisecon.stock.capital_flow import *


class TestPlateFlow(unittest.TestCase):

    def test_columns(self):
        """"""
        data = PlateFlow(days=1, size=10).load()
        pprint.pprint(data.to_dict(chinese_column=True)[0])
        print(data.metadata)

    def test_moke(self):
        """"""
        data = PlateFlow(days=1).load()
        data.show_columns()
        print(data.to_frame().to_markdown())
        print(data.to_frame(chinese_column=True).to_markdown())

    def test_market(self):
        """"""
        data = PlateFlow(market="沪深A股", days=1).load()
        print(data.metadata.response)
        print(data.to_frame(chinese_column=True).to_markdown())

    def test_plate_type_indu(self):
        """"""
        data = PlateFlow(plate_type="行业", days=1).load()
        print(data.metadata.response)
        print(data.to_frame(chinese_column=True).to_markdown())

    def test_plate_type_zone(self):
        """"""
        data = PlateFlow(plate_type="地区", days=1).load()
        print(data.metadata.response)
        print(data.to_frame(chinese_column=True).to_markdown())

    def test_plate_type_conception(self):
        """"""
        data = PlateFlow(plate_type="概念", days=1).load()
        print(data.metadata.response)
        print(data.to_frame(chinese_column=True).to_markdown())

    def test_plate_code_industry(self):
        """"""
        data = PlateFlow(plate_code="BK1027", days=1).load()
        print(data.metadata.response)
        print(data.to_frame(chinese_column=True).to_markdown())

    def test_plate_code_zone(self):
        """"""
        data = PlateFlow(plate_code="BK0158", days=1).load()
        print(data.metadata.response)
        print(data.to_frame(chinese_column=True).to_markdown())

    def test_plate_code_conception(self):
        """"""
        data = PlateFlow(plate_code="BK1044", days=1).load()
        print(data.metadata.response)
        print(data.to_frame(chinese_column=True).to_markdown())

    def test_sort(self):
        """"""
        data = PlateFlow(market="全部股票", sort_by="f184").load()
        print(data.to_frame(chinese_column=True).to_markdown())

    def test_plate_type_indu_sort(self):
        """"""
        data = PlateFlow(plate_type="行业", days=1, ascending=False).load()
        print(data.metadata.response)
        print(data.to_frame(chinese_column=True).to_markdown())

    def test_plate_type_indu_sort_true(self):
        """"""
        data = PlateFlow(plate_type="行业", days=1, ascending=True).load()
        print(data.metadata.response)
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

    def test_plate_history_conception(self):
        """"""
        data = CapitalFlowHistory(plate_code="BK1044", verbose=True, size=10).load()
        print(data.metadata.response)
        print(data.to_frame(chinese_column=True).to_markdown())

    def test_plate_history_zone(self):
        """BK0158"""
        data = CapitalFlowHistory(plate_code="BK0158", verbose=True, size=10).load()
        print(data.metadata.response)
        print(data.to_frame(chinese_column=True).to_markdown())

    def test_plate_history_industry(self):
        """BK1027"""
        data = CapitalFlowHistory(plate_code="BK1027", verbose=True, size=10).load()
        print(data.metadata.response)
        print(data.to_frame(chinese_column=True).to_markdown())

    def test_security_code(self):
        """"""
        data = CapitalFlowHistory(security_code="300750", size=10).load()
        print(data.metadata.response)
        print(data.to_frame(chinese_column=True).to_markdown())


class TestCurrentCapitalFlow(unittest.TestCase):
    """"""

    def test_market(self):
        """"""
        data = CapitalFlowCurrent(market="沪深两市", verbose=True, size=10).load()
        pprint.pprint(data.to_dict(chinese_column=True)[-1])
        print(data.metadata)
        print(data.to_frame(chinese_column=True).to_markdown())

    def test_market_sh(self):
        """"""
        data = CapitalFlowCurrent(market="沪市", verbose=True, size=10).load()
        print(data.to_markdown(chinese_column=True))

    def test_stock(self):
        """"""
        data = CapitalFlowCurrent(security_code=["601012", "300750"], verbose=True, size=10).load()
        pprint.pprint(data.to_dict(chinese_column=True)[-1])
        print(data.metadata)
        print(data.to_frame(chinese_column=True).to_markdown())

    def test_plate(self):
        """"""
        data = CapitalFlowCurrent(plate_code=["BK1044", "BK1027", "BK0158"], verbose=True, size=10).load()
        pprint.pprint(data.to_dict(chinese_column=True)[-1])
        print(data.metadata)
        print(data.to_frame(chinese_column=True).to_markdown())


class TestMinutesCapitalFlow(unittest.TestCase):

    def test_columns(self):
        """"""
        data = CapitalFlowMinutes(market="沪B", verbose=True, size=10).load()
        pprint.pprint(data.to_dict(chinese_column=True)[-1])
        print(data.metadata)

    def test_market_minutes(self):
        """"""
        data = CapitalFlowMinutes(market="沪深两市", verbose=True, size=10).load()
        print(data.to_frame().to_markdown())
        print(data.to_frame(chinese_column=True).to_markdown())

    def test_market_minutes_sh(self):
        """"""
        data = CapitalFlowMinutes(market="沪市", verbose=True, size=10).load()
        print(data.to_frame(chinese_column=True).to_markdown())

    def test_plate_minutes_conception(self):
        """"""
        data = CapitalFlowMinutes(plate_code="BK1044", verbose=True, size=10).load()
        print(data.metadata.response)
        print(data.to_frame(chinese_column=True).to_markdown())

    def test_plate_Minutes_zone(self):
        """BK0158"""
        data = CapitalFlowMinutes(plate_code="BK0158", verbose=True, size=10).load()
        print(data.metadata.response)
        print(data.to_frame(chinese_column=True).to_markdown())

    def test_plate_Minutes_industry(self):
        """BK1027"""
        data = CapitalFlowMinutes(plate_code="BK1027", verbose=True, size=10).load()
        print(data.metadata.response)
        print(data.to_frame(chinese_column=True).to_markdown())

    def test_security_code(self):
        """"""
        data = CapitalFlowMinutes(security_code="300750", size=10).load()
        print(data.metadata.response)
        print(data.to_frame(chinese_column=True).to_markdown())
