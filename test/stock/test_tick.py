
import unittest
from wisecon.stock.tick.tick import Tick


class TestTick(unittest.TestCase):

    def test_tick(self):
        data = Tick(code="301618").load()
        data.show_columns()
        print(data.to_frame(chinese_column=True).to_markdown())
