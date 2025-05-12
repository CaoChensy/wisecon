import unittest
from wisecon.report import *
from wisecon.mcp.report import *
import pandas as pd


class TestReport(unittest.TestCase):
    def test_stock_morning_news_report(self):
        """"""
        columns = ["reportType", "columnType", "title"]
        report = Report(report_type="券商晨报", size=100, begin_time="2024-09-23", end_time="2024-09-23")
        data = report.load()
        print(data.to_frame()[columns].to_markdown())

    def test_strategy_report(self):
        """"""
        columns = ["reportType", "columnType", "title"]
        report = Report(report_type="策略报告", size=50, begin_time="2024-09-23", end_time="2024-09-23")
        data = report.load()
        print(data.to_frame()[columns].to_markdown())

    def test_macro_report(self):
        """"""
        columns = ["reportType", "columnType", "title"]
        report = Report(report_type="宏观研究", size=5, begin_time="2024-09-23", end_time="2024-09-23")
        data = report.load()
        # print(data.to_frame()[columns].to_markdown())
        columns = ["title", "orgSName", "infoCode"]
        print(data.to_frame().to_markdown())

    def test_industry_report(self):
        """"""
        columns = ["industryName", "industryCode", "reportType", "title"]
        report = Report(report_type="行业研报", size=5, begin_time="2024-09-23", end_time="2024-09-23", verbose=True)
        data = report.load()
        print(data.to_frame()[columns].to_markdown())

    def test_industry_code_report(self):
        """"""
        columns = ["industryName", "industryCode", "reportType", "title"]
        report = Report(report_type="行业研报", industry_code="451", size=5, begin_time="2024-09-23", end_time="2024-09-23", verbose=True)
        data = report.load()
        # print(data.to_frame()[columns].to_markdown())
        columns = ["title", "orgSName", "infoCode"]
        print(data.to_frame()[columns].to_markdown())

    def test_stock_report(self):
        """"""
        columns = ["stockCode", "stockName", "reportType", "title"]
        report = Report(report_type="个股研报", size=500, begin_time="2024-09-23", end_time="2024-09-23", verbose=True)
        data = report.load()
        print(data.to_frame()[columns].to_markdown())

    def test_stock_code_report(self):
        """"""
        columns = ["stockCode", "stockName", "reportType", "title"]
        report = Report(code="002222", report_type="个股研报", size=500, begin_time="2024-09-23", end_time="2024-09-23", verbose=True)
        data = report.load()
        print(data.to_frame()[columns].to_markdown())

    def test_save_report(self):
        """"""
        report = Report(
            report_type="行业研报", industry_code="451", size=5, begin_time="2024-09-23",
            end_time="2024-09-23")
        content = report.to_text(info_code="AP202409231639991919")
        print(content)
        report.save_pdf(info_code="AP202409231639991919")

    def test_fetch_with_scrapy(self):
        """"""
        report = Report()
        data = report.to_bytes_content(info_code="AP202409231639991919", tool="scrapy")
        report = Report()
        data = report.to_bytes_content(info_code="AP202409231639991919", tool="scrapy")
        print(type(data), len(data))

    def test_fetch_with_request(self):
        """"""
        report = Report()
        data = report.to_bytes_content(info_code="AP202409231639991919", tool="request")
        print(type(data), len(data))

    def test_fetch_with_httpx(self):
        """"""
        report = Report()
        data = report.to_bytes_content(info_code="AP202409231639991919", tool="httpx")
        print(type(data), len(data))

    def test_range_report(self):
        """"""
        date = pd.date_range(start="2025-01-11", end="2025-02-14").astype(str).to_list()
        for d in date:
            print(d)
            report = Report(verbose=True, begin_time=d, end_time=d, size=100)
            report.save(path="/Users/chensy/Desktop/reports")

# class TestProfitForecast(unittest.TestCase):
#
#     def test_forecast(self):
#         """"""
#         report = ProfitForecast(size=2)
#         data = report.load_data()
#         columns = data.metadata.get("columns")
#         print(data.to_frame(columns=columns).to_markdown())
#
#     def test_forecast_by_industry(self):
#         """"""
#         report = ProfitForecast(industry="电源设备", size=2)
#         data = report.load_data()
#         columns = data.metadata.get("columns")
#         print(data.to_frame(columns=columns).to_markdown())
#
#     def test_forecast_by_conception(self):
#         """"""
#         report = ProfitForecast(conception="高压快充", size=2)
#         data = report.load_data()
#         columns = data.metadata.get("columns")
#         print(data.to_frame(columns=columns).to_markdown())
#
#     def test_forecast_by_district(self):
#         """"""
#         report = ProfitForecast(district="北京板块", size=2)
#         data = report.load_data()
#         columns = data.metadata.get("columns")
#         print(data.to_frame(columns=columns).to_markdown())
