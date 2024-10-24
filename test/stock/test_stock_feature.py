import unittest
from wisecon.types.columns import StockFeatures


class TestColumns(unittest.TestCase):

    def test_stock_features(self):
        stock_features = StockFeatures()
        stock_features._mapping(columns=["f31"])

    def test_stock_features_default(self):
        stock_features = StockFeatures()
        stock_features._mapping()

    def test_stock_features_all(self):
        stock_features = StockFeatures()
        stock_features._mapping(columns=[])
