import os
import unittest
import inspect
from wisecon.stock.etf import *
from wisecon.agent import *
from wisecon.types.agent import Function

# def gold_etf(
#         market:
# ):
#     """"""
#     data = ETFGoldHistory(market="ETF白银").load()
#     tool_list
#


class TestToolCall(unittest.TestCase):
    """"""
    def test_tools_sync(self):
        """"""
        base_url = "https://open.bigmodel.cn/api/paas/v4"
        tools = Tools(tools=[ETFGoldHistory])
        agent = BaseAgent(model="glm-4-flash", base_url=base_url, tools=tools, api_key_name="ZHIPU_API_KEY")
        completion = agent.chat(prompt="查询2023年12月1日的ETF白银历史数据")

    def test_tools_sync_chat(self):
        """"""
        base_url = "https://open.bigmodel.cn/api/paas/v4"
        tools = Tools(tools=[ETFGoldHistory])
        agent = BaseAgent(model="glm-4-flash", base_url=base_url, tools=tools, api_key_name="ZHIPU_API_KEY")
        completion = agent.chat(prompt="你好")

    def test_tools_sse(self):
        """"""
        base_url = "https://open.bigmodel.cn/api/paas/v4"
        tools = Tools(tools=[ETFGoldHistory])
        agent = BaseAgent(
            model="glm-4-flash", base_url=base_url, tools=tools, api_key_name="ZHIPU_API_KEY")
        completion = agent.chat(prompt="查询2023年12月1日的ETF白银历史数据", stream=True)
        answer = ""
        for chunk in completion:
            if chunk.choices[0].delta.content is None:
                answer += str(chunk.choices[0].delta.tool_calls[0].function.model_dump())
            else:
                answer += chunk.choices[0].delta.content
        print(answer)

    def test_tools_sse_chat(self):
        """"""
        base_url = "https://open.bigmodel.cn/api/paas/v4"
        tools = Tools(tools=[ETFGoldHistory])
        agent = BaseAgent(
            model="glm-4-flash", base_url=base_url, tools=tools, api_key_name="ZHIPU_API_KEY")
        completion = agent.chat(prompt="你好", stream=True)
        for chunk in completion:
            print(chunk)

    def test_etf_gold_bai(self):
        """"""
        data = ETFGoldHistory(market="ETF白银").load()
        print(data.to_frame(chinese_column=True).to_markdown())

    def test_etf_gold(self):
        """"""
        data = ETFGoldHistory(market="ETF黄金", date="2024-10-25").load()
        print(data.to_frame(chinese_column=True).to_markdown())

    def test_etf_gold_date(self):
        """"""
        data = ETFGoldHistory(market="ETF黄金", start_date="2024-10-25").load()
        print(data.to_frame(chinese_column=True).to_markdown())
