import unittest
from wisecon.utils.time import *


class TestTime(unittest.TestCase):
    def test_year_to_start_end(self):
        """"""
        start_date, end_date = year2date(2022, format="%Y-%m-%d")
        print(start_date, type(start_date), end_date, type(end_date))

    def test_get_quarter_ends(self):
        """"""
        result = get_quarter_ends('2023-03-31', '2024-03-31')
        print(result)

    def test_get_now_date(self):
        """"""
        result = get_now_date()
        print(result)

        result = get_now_date(format="%Y-%m-%d")
        print(result)
