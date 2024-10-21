from typing import Any, Dict, Literal, Callable, Optional
from wisecon.types import BaseMapping
from .base import *


__all__ = [
    "EarnFast",
    "EarnFastMapping",
]


class EarnFastMapping(BaseMapping):
    """"""
    columns: Dict = {
        "SECURITY_CODE": "证券代码",
        "SECURITY_NAME_ABBR": "证券简称",
        "TRADE_MARKET": "交易市场",
        "TRADE_MARKET_CODE": "交易市场代码",
        "SECURITY_TYPE": "证券类型",
        "SECURITY_TYPE_CODE": "证券类型代码",
        "UPDATE_DATE": "更新时间",
        "REPORT_DATE": "报告日期",
        "BASIC_EPS": "基本每股收益",
        "TOTAL_OPERATE_INCOME": "营业总收入",
        "TOTAL_OPERATE_INCOME_SQ": "去年同期营业总收入",
        "PARENT_NETPROFIT": "净利润",
        "PARENT_NETPROFIT_SQ": "去年同期净利润",
        "PARENT_BVPS": "每股净资产",
        "WEIGHTAVG_ROE": "净资产收益率",
        "YSTZ": "营业总收入同比增长率",
        "JLRTBZCL": "净利润同比增长率",
        "DJDYSHZ": "季度环比营业收入增长率",
        "DJDJLHZ": "季度环比净利润增长率",
        "PUBLISHNAME": "发布名称",
        "ORG_CODE": "机构代码",
        "NOTICE_DATE": "公告日期",
        "QDATE": "季度日期",
        "DATATYPE": "数据类型",
        "MARKET": "市场",
        "ISNEW": "是否最新",
        "EITIME": "导入时间",
        "SECUCODE": "证券代码"
    }


class EarnFast(StockFormRequestData):
    """业绩报表"""
    def __init__(
            self,
            security_code: Optional[str] = None,
            size: Optional[int] = 50,
            start_date: Optional[str] = None,
            end_date: Optional[str] = None,
            date: Optional[str] = None,
            industry_name: Optional[str] = None,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        """

        :param security_code: 600000
        :param size:
        :param start_date: 2024-09-30
        :param end_date: 2024-09-30
        :param date: 2024-09-30
        :param verbose:
        :param logger:
        :param kwargs:
        """
        self.security_code = security_code
        self.size = size
        self.start_date = start_date
        self.end_date = end_date
        self.date = date
        self.industry_name = industry_name
        self.mapping = EarnFastMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs
        self.request_set(response_type="json", description="股票业绩报表")
        self.conditions = []

    def params_filter(self) -> str:
        """
        :return:
        """
        self.filter_report_date()
        self.filter_security_code()
        if self.industry_name:
            self.conditions.append(f'(PUBLISHNAME="{self.industry_name}")')
        return "".join(self.conditions)

    def params(self) -> Dict:
        """
        :return:
        """
        params = {
            "filter": self.params_filter(),
            "sortColumns": "UPDATE_DATE,SECURITY_CODE",
            "sortTypes": "-1,-1",
            "pageSize": self.size,
            "pageNumber": 1,
            "reportName": "RPT_FCI_PERFORMANCEE",
        }
        return self.base_param(params)
