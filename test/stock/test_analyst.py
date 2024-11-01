import unittest
from wisecon.stock.analyst import *


class TestAnalyst(unittest.TestCase):
    """"""

    def test_year_rank(self):
        """"""
        data = AnalystYearRank(year="2024").load()
        print(data.to_markdown(chinese_column=True))

    def test_year_industry_rank(self):
        """"""
        data = AnalystYearRank(year="2024", industry_code="480000").load()
        print(data.to_markdown(chinese_column=True))


class TestAnalystIndex(unittest.TestCase):
    """"""

    def test_analyst_index(self):
        """"""
        data = AnalystIndex(analyst_code="11000280036").load()
        print(data.to_markdown(chinese_column=True))

    def test_analyst_stock_current(self):
        """"""
        data = ResearcherStock(analyst_code="11000280036", current=True).load()
        print(data.to_markdown(chinese_column=True))

    def test_analyst_stock_history(self):
        """"""
        data = ResearcherStock(analyst_code="11000280036", current=False).load()
        print(data.to_markdown(chinese_column=True))

