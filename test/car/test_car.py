import unittest
from wisecon.car import *


class TestCarBrand(unittest.TestCase):
    """"""
    def test_00(self):
        data = CarBrandList(verbose=True).load()
        print(data.to_frame(chinese_column=True))


class TestCarCurrent(unittest.TestCase):
    """"""
    def test_01(self):
        data = CurrentCarSales(data_type="销量", verbose=True).load()
        print(data.to_frame(chinese_column=True))

    def test_02(self):
        data = CurrentCarSales(data_type="车型级别", verbose=True).load()
        print(data.to_frame(chinese_column=True))

    def test_03(self):
        data = CurrentCarSales(data_type="厂商销量", verbose=True).load()
        print(data.to_frame(chinese_column=True))

    def test_04(self):
        data = CurrentCarSales(data_type="车型销量", verbose=True).load()
        print(data.to_frame(chinese_column=True))

    def test_05(self):
        data = CurrentCarSales(data_type="车身类别", verbose=True).load()
        print(data.to_frame(chinese_column=True))

    def test_06(self):
        data = CurrentCarSales(data_type="品牌销量", verbose=True).load()
        print(data.to_frame(chinese_column=True))

    def test_07(self):
        data = CurrentCarSales(data_type="电动车销量", verbose=True).load()
        print(data.to_frame(chinese_column=True))


class TestHistory(unittest.TestCase):
    """"""
    def test_html(self):
        """"""
        data = CarHistorySales(data_type="汽车销量").load()
        df = data.to_frame(chinese_column=True)
        print(df.shape)
        print(df.to_markdown())
