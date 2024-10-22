from typing import Any, Dict, Literal, Callable, Optional
from wisecon.types import BaseMapping
from .base import *


__all__ = [
    "FreeHolder",
    "FreeHolderMapping",
]


TypeMarket = Literal["沪深A股", "沪市A股", "科创板", "深市A股", "创业板", "京市A股"]


class FreeHolderMapping(BaseMapping):
    """"""
    columns: Dict = {
        "SECUCODE": "证券代码",
        "SECURITY_CODE": "证券代码",
        "ORG_CODE": "机构代码",
        "END_DATE": "截止日期",
        "HOLDER_NAME": "股东名称",
        "HOLD_NUM": "持有股数",
        "FREE_HOLDNUM_RATIO": "自由持股比例",
        "HOLD_NUM_CHANGE": "持股变动",
        "CHANGE_RATIO": "变动比例",
        "IS_HOLDORG": "是否持股机构",
        "HOLDER_RANK": "股东排名",
        "SECURITY_NAME_ABBR": "证券简称",
        "HOLDER_CODE": "股东代码",
        "SECURITY_TYPE_CODE": "证券类型代码",
        "HOLDER_STATE": "股东状态",
        "HOLDER_MARKET_CAP": "股东市值",
        "HOLD_RATIO": "持股比例",
        "HOLD_CHANGE": "持股变动",
        "HOLD_RATIO_CHANGE": "持股比例变动",
        "HOLDER_TYPE": "股东类型",
        "SHARES_TYPE": "股份类型",
        "UPDATE_DATE": "更新时间",
        "REPORT_DATE_NAME": "报告名称",
        "HOLDER_NEW": "新的股东",
        "FREE_RATIO_QOQ": "自由持股比例环比",
        "HOLDER_STATEE": "股东状态",
        "IS_REPORT": "是否报告",
        "HOLDER_CODE_OLD": "旧股东代码",
        "HOLDER_NEWTYPE": "新股东类型",
        "HOLDNUM_CHANGE_NAME": "持股变动名称",
        "IS_MAX_REPORTDATE": "是否为最新报告日期",
        "COOPERATION_HOLDER_MARK": "合作股东标识",
        "MXID": "记录ID",
        "LISTING_STATE": "上市状态",
        "XZCHANGE": "新增变动",
        "NEW_CHANGE_RATIO": "新变动比例",
        "HOLDER_STATE_NEW": "新的股东状态",
        "HOLD_ORG_CODE_SOURCE": "持股机构来源代码"
    }


class FreeHolder(StockFormRequestData):
    """"""
    def __init__(
            self,
            security_code: Optional[str] = None,
            holder_type: Optional[Literal["个人", "基金", "QFII", "社保", "券商", "信托"]] = None,
            holder_change: Optional[Literal["增加", "不变", "减少"]] = None,
            size: Optional[int] = 50,
            start_date: Optional[str] = None,
            end_date: Optional[str] = None,
            date: Optional[str] = None,
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
        self.holder_type = holder_type
        self.holder_change = holder_change
        self.size = size
        self.start_date = start_date
        self.end_date = end_date
        self.date = date
        self.mapping = FreeHolderMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs
        self.request_set(response_type="json", description="上市公司十大流通股东")
        self.conditions = []

    def params_filter(self) -> str:
        """"""
        self.filter_report_date(date_name="END_DATE")
        self.filter_security_code()
        if self.holder_type:
            self.conditions.append(f'(HOLDER_NEWTYPE="{self.holder_type}")')
        if self.holder_change:
            self.conditions.append(f'(HOLDNUM_CHANGE_NAME="{self.holder_change}")')
        return "".join(self.conditions)

    def params(self) -> Dict:
        """
        :return:
        """
        params = {
            "filter": self.params_filter(),
            "sortColumns": "UPDATE_DATE,SECURITY_CODE,HOLDER_RANK",
            "sortTypes": "-1,1,1",
            "pageSize": self.size,
            "pageNumber": 1,
            "reportName": "RPT_F10_EH_FREEHOLDERS",
        }
        return self.base_param(params)