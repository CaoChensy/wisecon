from typing import Any, Dict, Literal, Callable, Optional
from wisecon.types import BaseMapping
from .base import *


__all__ = [
    "FreeHolderChange",
    "FreeHolderChangeMapping",
]


class FreeHolderChangeMapping(BaseMapping):
    """"""
    columns: Dict = {
        "HOLDER_NEW": "新的股东",
        "END_DATE": "截止日期",
        "HOLDER_NAME": "股东名称",
        "HOLDER_CODE": "股东代码",
        "HOLDER_TYPE": "股东类型",
        "REPORT_DATE_NAME": "报告名称",
        "HOLDER_SOURCE_CODE": "股东来源代码",
        "HOLDER_SOURCE": "股东来源",
        "HOLDER_NUM": "持有股数",
        "HOLDADD_NUM": "增持股数",
        "HOLDUP_NUM": "持股增加数",
        "HOLDDOWN_NUM": "持股减少数",
        "HOLDUNCHANGED_NUM": "持股不变数",
        "IS_REPORT": "是否报告",
        "HOLDER_MARKET_CAP": "股东市值",
        "SEAB_JOIN": "关联股票",
        "CLOSE_PRICE": "收盘价",
        "IS_MAX_REPORTDATE": "是否为最新报告日期"
    }


class FreeHolderChange(StockFormRequestData):
    """"""
    def __init__(
            self,
            holder_name: Optional[str] = None,
            holder_type: Optional[Literal["个人", "基金", "QFII", "社保", "券商", "信托"]] = None,
            size: Optional[int] = 50,
            start_date: Optional[str] = None,
            end_date: Optional[str] = None,
            date: Optional[str] = None,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        """

        :param size:
        :param start_date: 2024-09-30
        :param end_date: 2024-09-30
        :param date: 2024-09-30
        :param verbose:
        :param logger:
        :param kwargs:
        """
        self.holder_name = holder_name
        self.holder_type = holder_type
        self.size = size
        self.start_date = start_date
        self.end_date = end_date
        self.date = date
        self.mapping = FreeHolderChangeMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs
        self.request_set(response_type="json", description="十大流通股东持股变动统计")
        self.conditions = []

    def params_filter(self) -> str:
        """"""
        self.filter_report_date(date_name="END_DATE")
        if self.holder_type:
            self.conditions.append(f'(HOLDER_TYPE="{self.holder_type}")')
        if self.holder_name:
            self.conditions.append(f'(HOLDER_NAME+like+"%{self.holder_name}%")')
        return "".join(self.conditions)

    def params(self) -> Dict:
        """
        :return:
        """
        params = {
            "filter": self.params_filter(),
            "sortColumns": "HOLDER_NUM,HOLDER_NEW",
            "sortTypes": "-1,-1",
            "pageSize": self.size,
            "pageNumber": 1,
            "reportName": "RPT_FREEHOLDERS_BASIC_INFONEW",
        }
        return self.base_param(params)