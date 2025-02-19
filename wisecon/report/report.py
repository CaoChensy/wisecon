from typing import Any, Dict, Union, Callable, Optional
from wisecon.types import BaseMapping
from wisecon.types.request_api.report import *


__all__ = [
    "ReportMapping",
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
            report_type: Optional[TypeReport] = "*",
            q_type: Optional[Union[int, str]] = None,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        """

        Args:
            code:
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
