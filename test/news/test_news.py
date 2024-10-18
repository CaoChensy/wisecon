import unittest
from wisecon.report.news import *


class TestNews(unittest.TestCase):
    def test_news(self):
        news = News(size=20)
        data = news.load_data()

        print(data.metadata)
        self.assertIsNotNone(data)
        print(data.to_frame(columns=data.metadata.get("columns")).to_markdown())

