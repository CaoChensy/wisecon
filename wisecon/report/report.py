import os
import time
import requests
from typing import Any, List, Dict, Union, Callable, Literal, Optional
from wisecon.types import BaseMapping, APIReportRequest, TypeReport, ReportData
from wisecon.utils import tqdm_progress_bar
from lumix.documents import StructuredPDF

__all__ = [
    "Report",
]


class ReportMapping(BaseMapping):
    """"""
    columns: Dict = {
        "title": "标题",
        "stockName": "股票名称",
        "stockCode": "股票代码",
        "orgCode": "机构代码",
        "orgName": "机构名称",
        "orgSName": "机构简称",
        "publishDate": "发布日期",
        "infoCode": "信息编码",
        "column": "栏目",
        "predictNextTwoYearEps": "预测未来两年每股收益",
        "predictNextTwoYearPe": "预测未来两年市盈率",
        "predictNextYearEps": "预测下一年每股收益",
        "predictNextYearPe": "预测下一年市盈率",
        "predictThisYearEps": "预测今年每股收益",
        "predictThisYearPe": "预测今年市盈率",
        "predictLastYearEps": "预测去年每股收益",
        "predictLastYearPe": "预测去年市盈率",
        "actualLastTwoYearEps": "实际过去两年每股收益",
        "actualLastYearEps": "实际去年每股收益",
        "industryCode": "行业编码",
        "industryName": "行业名称",
        "emIndustryCode": "细分行业编码",
        "indvInduCode": "个体行业编码",
        "indvInduName": "个体行业名称",
        "emRatingCode": "评级编码",
        "emRatingValue": "评级值",
        "emRatingName": "评级名称",
        "lastEmRatingCode": "最近评级编码",
        "lastEmRatingValue": "最近评级值",
        "lastEmRatingName": "最近评级名称",
        "ratingChange": "评级变动",
        "reportType": "报告类型",
        "author": "作者",
        "indvIsNew": "个体是否为新",
        "researcher": "研究员",
        "newListingDate": "新上市日期",
        "newPurchaseDate": "新购买日期",
        "newIssuePrice": "新发行价格",
        "newPeIssueA": "新市盈率发行A",
        "indvAimPriceT": "个体目标价格T",
        "indvAimPriceL": "个体目标价格L",
        "attachType": "附件类型",
        "attachSize": "附件大小",
        "attachPages": "附件页数",
        "encodeUrl": "编码网址",
        "sRatingName": "综合评级名称",
        "sRatingCode": "综合评级编码",
        "market": "市场",
        "authorID": "作者ID",
        "count": "计数",
        "orgType": "机构类型"
    }


class Report(APIReportRequest):
    """"""
    def __init__(
            self,
            code: Optional[str] = None,
            industry: Optional[str] = "*",
            industry_code: Optional[Union[str, int]] = "*",
            size: Optional[int] = 5,
            rating: Optional[str] = "*",
            rating_change: Optional[str] = "*",
            begin_time: Optional[str] = "*",
            end_time: Optional[str] = "*",
            page_no: Optional[int] = 1,
            report_type: Optional[TypeReport] = None,
            q_type: Optional[Union[int, str]] = None,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        """

        Args:
            code: 股票代码
            industry:
            industry_code:
            size:
            rating:
            rating_change:
            begin_time:
            end_time:
            page_no:
            report_type:
            q_type:
            verbose:
            logger:
            **kwargs:
        """
        self.code = code
        self.industry = industry
        self.industry_code = industry_code
        self.size = size
        self.rating = rating
        self.rating_change = rating_change
        self.begin_time = begin_time
        self.end_time = end_time
        self.page_no = page_no
        self.report_type = report_type
        self.q_type = q_type
        self.mapping = ReportMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs
        self.request_set(
            response_type="json",
            description="投研报告",
        )

    def params(self) -> Dict:
        """"""
        if self.q_type is None:
            self.reports_type()

        params = {
            "industry": self.industry,
            "industryCode": self.industry_code,
            "pageSize": self.size,
            "rating": self.rating,
            "ratingChange": self.rating_change,
            "beginTime": self.begin_time,
            "endTime": self.end_time,
            "pageNo": self.page_no,
            "qType": self.q_type,
            "_": self.current_time()
        }
        if self.code:
            params.update({"code": self.code})
        return self.base_param(update=params)

    def bytes_file(
            self,
            info_codes: List[str]
    ):
        """"""
        self.reports_data = []
        base_url = """https://pdf.dfcfw.com/pdf/H3_{}_1.pdf""".format
        for info_code in tqdm_progress_bar(info_codes):
            _report = ReportData(code=info_code)
            try:
                response = requests.get(base_url(info_code), headers=self.headers)
                _report.content = response.content
            except Exception as e:
                self._logger(msg=f"[{__class__.__name__}] Load `{info_code}` error, error message: {e}", color="red")
                _report.error = str(e)
            self.reports_data.append(_report)

    def to_bytes_content(self, info_code: str, tool: Literal["request", "scrapy", "httpx", "selenium"] = "request") -> bytes:
        """"""
        base_url = f"""https://pdf.dfcfw.com/pdf/H3_{info_code}_1.pdf"""
        try:
            if tool == "request":
                self._logger(msg=f"[{__class__.__name__}] Use: {tool}")
                response = requests.get(base_url, headers=self.headers)
                return response.content
            elif tool == "scrapy":
                from wisecon.utils.fetch_pdf import fetch_pdf_bytes
                self._logger(msg=f"[{__class__.__name__}] Use: {tool}")
                response = fetch_pdf_bytes(base_url, headers=self.headers)
                return response
            elif tool == "httpx":
                import httpx
                with httpx.Client(headers=self.headers, http2=False) as client:
                    response = client.get(base_url, headers=self.headers)
                return response.content
            elif tool == "selenium":
                from wisecon.utils.fetch_pdf import fetch_pdf_bytes_use_selenium
                return fetch_pdf_bytes_use_selenium(base_url)

        except Exception as e:
            msg = f"[{__class__.__name__}] Load `{info_code}` error, error message: {e}"
            self._logger(msg=msg, color="red")
            raise Exception(msg)

    def to_text(self, info_code: str, tool: Literal["request", "scrapy", "httpx", "selenium"] = "request") -> str:
        """"""
        bytes_data = self.to_bytes_content(info_code=info_code, tool=tool)
        pdf = StructuredPDF(path_or_data=bytes_data)
        return pdf.to_text()

    def save_pdf(self, info_code: str, path: Optional[str] = None, tool: Literal["request", "scrapy", "httpx", "selenium"] = "request"):
        """"""
        if path is None:
            path = f"{info_code}.pdf"
        bytes_data = self.to_bytes_content(info_code=info_code, tool=tool)
        with open(path, "wb") as f:
            f.write(bytes_data)

    def save(
            self,
            path: str = "./reports",
            info_codes: Optional[List[str]] = None,
    ):
        """"""
        if not os.path.exists(path):
            os.makedirs(path)
        cache_path = os.path.join(path, "cache")
        if not os.path.exists(cache_path):
            os.makedirs(cache_path)
        pdf_path = cache_path = os.path.join(path, "pdf")
        if not os.path.exists(pdf_path):
            os.makedirs(pdf_path)

        if info_codes is None:
            response_data = self.load()
            if len(response_data.data) > 0:
                report_data = response_data.to_frame()
                info_codes = report_data["infoCode"].tolist()
                report_data.to_csv(os.path.join(cache_path, f"{str(int(time.time() * 1E3))}.csv"), index=False)
            else:
                info_codes = []
                self._logger(msg=f"[{__class__.__name__}] Not find report.")
        if len(info_codes) > 0:
            self.bytes_file(info_codes=info_codes)
            for _report in self.reports_data:
                if isinstance(_report.content, bytes):
                    file_path = os.path.join(pdf_path, f"{_report.code}.pdf")
                    with open(file_path, "wb") as f:
                        f.write(_report.content)


def report_info(
            code: Optional[str] = None,
            industry: Optional[str] = "*",
            industry_code: Optional[Union[str, int]] = "*",
            size: Optional[int] = 5,
            rating: Optional[str] = "*",
            rating_change: Optional[str] = "*",
            begin_time: Optional[str] = "*",
            end_time: Optional[str] = "*",
            page_no: Optional[int] = 1,
            report_type: Optional[TypeReport] = None,
            q_type: Optional[Union[int, str]] = None,
):
    """"""
    report = Report(
        code=code, industry=industry, industry_code=industry_code, size=size,
        rating=rating, rating_change=rating_change, begin_time=begin_time,
        end_time=end_time, page_no=page_no, report_type=report_type, q_type=q_type
    )
    columns = [

    ]
    data = report.load().to_frame(chinese_column=True)
    return data.to_markdown(index=False)
