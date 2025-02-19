import unittest
from wisecon.report.report import *
import pandas as pd


class TestReport(unittest.TestCase):
    """"""
    def test_report_list(self):
        """"""
        report = Report(verbose=True)
        report.save(path="./reports")

    def test_report_date_length(self):
        """
        Returns:

        """
        report = Report(verbose=True)
        report.save(path="./reports")

    def test_range_report(self):
        """"""
        date = pd.date_range(start="2025-01-11", end="2025-02-14").astype(str).to_list()
        for d in date:
            print(d)
            report = Report(verbose=True, begin_time=d, end_time=d, size=100)
            report.save(path="/Users/chensy/Desktop/reports")
