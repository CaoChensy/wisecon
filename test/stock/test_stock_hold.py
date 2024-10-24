import unittest
from pprint import pprint
from wisecon.stock.holder import *


class TestFreeHolder(unittest.TestCase):

    def test_columns(self):
        """"""
        data = FreeHolder(start_date="2024-09-30", size=1).load()
        pprint(data.to_dict(chinese_column=True)[0], indent=4)

    def test_load(self):
        """
        :return:
        """
        data = FreeHolder(start_date="2024-09-30", size=5, verbose=True).load()
        data.show_columns()
        print(data.to_frame(chinese_column=True).to_markdown())

    def test_stock(self):
        """
        :return:
        """
        data = FreeHolder(start_date="2024-06-30", security_code="000766", size=10, verbose=True).load()
        data.show_columns()
        print(data.to_frame(chinese_column=True).to_markdown())


class TestHolder(unittest.TestCase):

    def test_columns(self):
        """"""
        data = Holder(start_date="2024-09-30", size=4).load()
        pprint(data.to_dict(chinese_column=True)[3], indent=4)

    def test_load(self):
        """
        :return:
        """
        data = Holder(start_date="2024-09-30", size=5, verbose=True).load()
        data.show_columns()
        print(data.to_frame(chinese_column=True).to_markdown())

    def test_stock(self):
        """
        :return:
        """
        data = Holder(start_date="2024-06-30", security_code="000766", size=10, verbose=True).load()
        data.show_columns()
        print(data.to_frame(chinese_column=True).to_markdown())


class TestFreeHolderChange(unittest.TestCase):

    def test_columns(self):
        """"""
        data = FreeHolderChange(start_date="2015-03-31", size=50, verbose=True).load()
        pprint(data.to_dict(chinese_column=True)[0], indent=4)

    def test_load(self):
        """
        :return:
        """
        data = FreeHolderChange(start_date="2015-03-31", size=5, verbose=True).load()
        data.show_columns()
        print(data.to_frame(chinese_column=True).to_markdown())

    def test_stock(self):
        """
        :return:
        """
        data = FreeHolderChange(start_date="2015-03-31", holder_name="工商银行", size=10, verbose=True).load()
        data.show_columns()
        print(data.to_frame(chinese_column=True).to_markdown())


class TestHolderChange(unittest.TestCase):

    def test_columns(self):
        """"""
        data = HolderChange(start_date="2015-03-31", size=50, verbose=True).load()
        pprint(data.to_dict(chinese_column=True)[0], indent=4)

    def test_load(self):
        """
        :return:
        """
        data = HolderChange(start_date="2015-03-31", size=5, verbose=True).load()
        data.show_columns()
        print(data.to_frame(chinese_column=True).to_markdown())

    def test_stock(self):
        """
        :return:
        """
        data = HolderChange(start_date="2015-03-31", holder_name="工商银行", size=10, verbose=True).load()
        data.show_columns()
        print(data.to_frame(chinese_column=True).to_markdown())


class TestFreeHolderStock(unittest.TestCase):

    def test_columns(self):
        """"""
        data = FreeHolderStock(start_date="2024-09-30", size=5, verbose=True).load()
        pprint(data.to_dict(chinese_column=True)[3], indent=4)

    def test_load(self):
        """
        :return:
        """
        data = FreeHolderStock(start_date="2024-09-30", size=5, verbose=True).load()
        data.show_columns()
        print(data.to_frame(chinese_column=True).to_markdown())

    def test_stock(self):
        """
        :return:
        """
        data = FreeHolderStock(start_date="2024-09-30", holder_name="工商银行", size=10, verbose=True).load()
        data.show_columns()
        print(data.to_frame(chinese_column=True).to_markdown())


class TestHolderStock(unittest.TestCase):

    def test_columns(self):
        """"""
        data = HolderStock(start_date="2024-09-30", size=5, verbose=True).load()
        pprint(data.to_dict(chinese_column=True)[3], indent=4)

    def test_load(self):
        """
        :return:
        """
        data = HolderStock(start_date="2024-09-30", size=5, verbose=True).load()
        data.show_columns()
        print(data.to_frame(chinese_column=True).to_markdown())

    def test_stock(self):
        """
        :return:
        """
        data = HolderStock(start_date="2024-09-30", holder_name="工商银行", size=10, verbose=True).load()
        data.show_columns()
        print(data.to_frame(chinese_column=True).to_markdown())


class TestFreeHolderStockAnalysis(unittest.TestCase):

    def test_columns(self):
        """"""
        data = FreeHolderStockAnalysis(start_date="2015-03-31", size=5).load()
        pprint(data.to_dict(chinese_column=True)[0], indent=4)

    def test_load(self):
        """
        :return:
        """
        data = FreeHolderStockAnalysis(start_date="2015-03-31", size=5, verbose=True).load()
        data.show_columns()
        print(data.to_frame(chinese_column=True).to_markdown())

    def test_stock(self):
        """
        :return:
        """
        data = FreeHolderStockAnalysis(start_date="2015-03-31", holder_name="工商银行", size=10, verbose=True).load()
        data.show_columns()
        print(data.to_frame(chinese_column=True).to_markdown())


class TestHolderStockAnalysis(unittest.TestCase):

    def test_columns(self):
        """"""
        data = HolderStockAnalysis(start_date="2015-03-31", size=5).load()
        pprint(data.to_dict(chinese_column=True)[0], indent=4)

    def test_load(self):
        """
        :return:
        """
        data = HolderStockAnalysis(start_date="2015-03-31", size=5, verbose=True).load()
        data.show_columns()
        print(data.to_frame(chinese_column=True).to_markdown())

    def test_stock(self):
        """
        :return:
        """
        data = HolderStockAnalysis(start_date="2015-03-31", holder_name="工商银行", size=10, verbose=True).load()
        data.show_columns()
        print(data.to_frame(chinese_column=True).to_markdown())


class TestFreeHolderCoop(unittest.TestCase):

    def test_columns(self):
        """"""
        data = FreeHolderCoop(size=5).load()
        pprint(data.to_dict(chinese_column=True)[0], indent=4)

    def test_load(self):
        """
        :return:
        """
        data = FreeHolderCoop(size=5).load()
        data.show_columns()
        print(data.to_frame(chinese_column=True).to_markdown())

    def test_stock(self):
        """
        :return:
        """
        data = FreeHolderCoop(holder_name="工商银行", size=10).load()
        data.show_columns()
        print(data.to_frame(chinese_column=True).to_markdown())


class TestHolderCoop(unittest.TestCase):

    def test_columns(self):
        """"""
        data = HolderCoop(size=5).load()
        pprint(data.to_dict(chinese_column=True)[0], indent=4)

    def test_load(self):
        """
        :return:
        """
        data = HolderCoop(size=5).load()
        data.show_columns()
        print(data.to_frame(chinese_column=True).to_markdown())

    def test_stock(self):
        """
        :return:
        """
        data = HolderCoop(holder_name="工商银行", size=10).load()
        data.show_columns()
        print(data.to_frame(chinese_column=True).to_markdown())
