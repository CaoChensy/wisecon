import unittest
from wisecon.stock.plate_mapping import *


class TestPlateMapping(unittest.TestCase):
    def test_plate_industry(self):
        data = PlateCode(plate_type="行业").load()
        print(data.to_frame(chinese_column=True).to_markdown())

    def test_plate_zone(self):
        data = PlateCode(plate_type="地区").load()
        print(data.to_frame(chinese_column=True).to_markdown())

    def test_plate_conception(self):
        data = PlateCode(plate_type="概念", verbose=True).load()
        print(data.to_frame(chinese_column=True).to_markdown())

    def test_industry_code(self):
        data = IndustryCode(verbose=True).load()
        print(data.to_markdown(chinese_column=True))
