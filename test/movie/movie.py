import unittest
from wisecon.movie import *
from wisecon.agent import *


class TestMovie(unittest.TestCase):
    """"""

    def test_tv_0(self):
        """"""
        data = TV(source="央视").load()
        print(data.to_markdown(chinese_column=True))

    def test_tv_1(self):
        """"""
        data = TV(source="卫视").load()
        print(data.to_markdown(chinese_column=True))

    def test_movie(self):
        """"""
        data = Movie().load()
        print(data.to_markdown(chinese_column=True))

    def test_movie_params(self):
        """"""
        data = Movie(verbose=True).load()
        print(data.to_markdown(chinese_column=True))

    def test_tools(self):
        """"""
        base_url = "https://open.bigmodel.cn/api/paas/v4"
        tools = Tools(tools=[Movie, TV])
        agent = BaseAgent(model="glm-4-flash", base_url=base_url, tools=tools, api_key_name="ZHIPU_API_KEY")
        completion = agent.chat(prompt="现在央视收视率最高的节目是？")
