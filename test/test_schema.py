import unittest
from wisecon.types.columns import StockFeatures


class TestColumns(unittest.TestCase):
    def test_stock_features(self):
        stock_features = StockFeatures()
        stock_features._mapping(columns=["f31"])


