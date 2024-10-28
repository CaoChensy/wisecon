import unittest
from wisecon.stock.ranking import *


class TestStockRanking(unittest.TestCase):

    def test_institution_ranking(self):
        """"""
        data = InstitutionRank(start_date="2024-10-23").load()
        print(data.to_frame(chinese_column=True).to_markdown())

    def test_stock_ranking(self):
        """"""
        data = StockRank(statistics_cycle="1m").load()
        print(data.to_frame(chinese_column=True).to_markdown())
