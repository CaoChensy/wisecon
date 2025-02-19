
import unittest
from wisecon.stock.tick.tick import Tick


class TestTick(unittest.TestCase):

    def test_tick(self):
        data = Tick(code="301618", verbose=True).load()
        data.show_columns()
        print(data.to_frame(chinese_column=True).to_markdown())

    def test_tick_1(self):
        data = Tick(code="300059", verbose=True).load()
        data.show_columns()
        print(data.to_frame(chinese_column=True).to_markdown())

    def test_tick_2(self):
        data = Tick(code="002249", verbose=True).load()
        data.show_columns()
        print(data.to_frame(chinese_column=True).to_markdown())
