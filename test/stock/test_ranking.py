import unittest
from wisecon.stock.ranking import *


class TestStockRanking(unittest.TestCase):
    """
    机构席位追踪每日活跃营业部营业部排行营业部统计营业部查询

    """
    def test_stock_ranking_detail(self):
        """龙虎榜详情"""
        data = StockRankDetail(date="2024-10-28").load()
        print(data.to_frame(chinese_column=True).to_markdown())

    def test_stock_ranking_detail_with_market(self):
        """龙虎榜详情"""
        data = StockRankDetail(market="沪市A股", date="2024-10-28").load()
        print(data.to_frame(chinese_column=True).to_markdown())

    def test_stock_ranking_statistic(self):
        """个股上榜统计"""
        data = StockRankStatistic(statistics_cycle="1m").load()
        print(data.to_frame(chinese_column=True).to_markdown())

    def test_institution_ranking(self):
        """机构买卖每日统计"""
        data = InstitutionTradeRank(start_date="2024-10-23").load()
        print(data.to_frame(chinese_column=True).to_markdown())

    def test_institution_seat(self):
        """机构席位追踪"""
        data = InstitutionSeat(statistics_cycle="1m").load()
        print(data.to_frame(chinese_column=True).to_markdown())

    def test_department_active(self):
        """"""
        data = DepartmentActive(date="2024-10-28").load()
        print(data.to_frame(chinese_column=True).to_markdown())

    def test_department_rank(self):
        """"""
        data = DepartmentRank(statistics_cycle="1m").load()
        print(data.to_frame(chinese_column=True).to_markdown())

    def test_department_statistic(self):
        """"""
        data = DepartmentStatistic(statistics_cycle="1m").load()
        print(data.to_frame(chinese_column=True).to_markdown())
