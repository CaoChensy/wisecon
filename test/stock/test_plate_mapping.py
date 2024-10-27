import unittest
from wisecon.stock.plate_mapping import PlateCode


class TestPlateMapping(unittest.TestCase):
    def test_get_plate(self):
        data = PlateCode(plate_type="行业").load()
        print(data.to_frame(chinese_column=True).to_markdown())
        