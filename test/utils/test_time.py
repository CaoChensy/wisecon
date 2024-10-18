import unittest
from wisecon.utils.time import *


class TestTime(unittest.TestCase):
    def test_year_to_start_end(self):
        """"""
        start_date, end_date = year2date(2022, format="%Y-%m-%d")
        print(start_date, type(start_date), end_date, type(end_date))
