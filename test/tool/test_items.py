import unittest
from wisecon.agent import *
from wisecon.movie import *
from wisecon.stock.etf import *
from wisecon.stock.market import *
from wisecon.stock.financial import *
from wisecon.stock.kline import *
from wisecon.stock.tick import *


class TestToolCall(unittest.TestCase):
    """"""
    def setUp(self):
        base_url = "https://open.bigmodel.cn/api/paas/v4"
        tools = Tools(tools=[
            LastDayMarketSummary,
            KLine,
            KlineMin,
            Tick,
            StockBalance,
            ETFGoldHistory,
            TV, Movie])
        self.agent = BaseAgent(
            model="glm-4-plus", base_url=base_url, tools=tools,
            api_key_name="ZHIPU_API_KEY")

    def test_gold_history(self):
        """"""
        completion = self.agent.chat(prompt="查询2023年12月1日的ETF白银历史数据")

    def test_tv(self):
        """"""
        completion = self.agent.chat(prompt="查询目前央视最受喜欢的节目")

    def test_movie(self):
        """"""
        completion = self.agent.chat(prompt="现在最受新欢的电影是哪部")

    def test_balance(self):
        """"""
        completion = self.agent.chat(prompt="2024年第三季度末纺织服装行业资产负债表前五名是多少？")

    def test_kline(self):
        """"""
        # completion = self.agent.chat(prompt="当前300069股票的价格是多少？")
        completion = self.agent.chat(prompt="当前300069股票最近5分钟的最低价价格是多少？")

    def test_kline_min(self):
        """"""
        completion = self.agent.chat(prompt="当前300069股票最近1分钟的最低价价格是多少？")

    def test_tick(self):
        """"""
        completion = self.agent.chat(prompt="当前300069股票的tick数据？")

    # def

