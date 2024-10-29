from typing import Any, Dict, Literal, Callable, Optional
from wisecon.types import BaseMapping, APIDataV1RequestData


__all__ = [
    "Holder",
    "HolderMapping",
]


class HolderMapping(BaseMapping):
    """字段映射 上市公司十大股东持股明细"""
    columns: Dict = {
        "SECUCODE": "证券代码",
        "SECURITY_CODE": "证券代码",
        "ORG_CODE": "机构代码",
        "SECURITY_TYPE_CODE": "证券类型代码",
        "END_DATE": "截止日期",
        "RANK": "排名",
        "HOLDER_CODE": "股东名称",
        "HOLDER_NAME": "股东姓名",
        "HOLD_NUM": "持有股数",
        "HOLD_RATIO": "持股比例(占流通)",
        "HOLD_NUM_CHANGE": "持股变动数",
        "HOLD_RATIO_CHANGE": "持股比例变动",
        "DIRECTION": "变动方向",
        "SHARES_TYPE": "股份类型",
        "HOLDER_NATURE": "股东性质",
        "REPORT_TYPE": "报告类型",
        "HOLD_CHANGE": "持股变动",
        "NOTICE_DATE": "公告日期",
        "HOLD_RATIO_YOY": "持股比例同比",
        "REPORT_DATE_NAME": "报告名称",
        "HOLDER_NEW": "新的股东",
        "SECURITY_NAME_ABBR": "证券简称",
        "HOLDNUM_CHANGE_RATIO": "持股变动比例",
        "IS_MAX_REPORTDATE": "是否为最新报告日期",
        "HOLDER_MARKET_CAP": "股东市值",
        "HOLDNUM_CHANGE_NAME": "持股变动名称",
        "MXID": "记录ID",
        "HOLDER_NEWTYPE": "新股东类型",
        "XZCHANGE": "期末持股数量变化(股)",
        "HOLDER_TYPE_ORG": "股东类型（机构）",
        "HOLD_RATIO_DIRECTION": "持股比例变动方向",
        "REFERENCE_MARKET_CAP": "参考市值",
        "HOLD_ORG_CODE_SOURCE": "持股机构来源代码"
    }


class Holder(APIDataV1RequestData):
    """查询 上市公司十大股东持股明细"""
    def __init__(
            self,
            holder_name: Optional[str] = None,
            security_code: Optional[str] = None,
            holder_type: Optional[Literal["个人", "基金", "QFII", "社保", "券商", "信托"]] = None,
            holder_change: Optional[Literal["新进", "增加", "不变", "减少"]] = None,
            size: Optional[int] = 50,
            start_date: Optional[str] = None,
            end_date: Optional[str] = None,
            date: Optional[str] = None,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        """
        Notes:
            ```python
            from wisecon.stock.holder import *

            data = Holder(size=20, start_date="2024-09-30").load()
            data.to_frame(chinese_column=True)
            ```

        Args:
            holder_name: 股东名称
            security_code: 股票代码
            holder_type: 股东类型 `["个人", "基金", "QFII", "社保", "券商", "信托"]`
            holder_change: 持股变动 `["新进", "增加", "不变", "减少"]`
            size: 返回条数
            start_date: 开始日期
            end_date: 结束日期
            date: 指定日期
            verbose: 是否显示日志
            logger: 自定义日志
            **kwargs: 其他参数
        """
        self.holder_name = holder_name
        self.security_code = security_code
        self.holder_type = holder_type
        self.holder_change = holder_change
        self.size = size
        self.start_date = start_date
        self.end_date = end_date
        self.date = date
        self.mapping = HolderMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs
        self.request_set(response_type="json", description="上市公司十大股东持股明细")
        self.conditions = []

    def params_filter(self) -> str:
        """"""
        self.filter_report_date(date_name="END_DATE")
        self.filter_security_code()
        if self.holder_type:
            self.conditions.append(f'(HOLDER_TYPE="{self.holder_type}")')
        if self.holder_name:
            self.conditions.append(f'(HOLDER_NAME+like+"%{self.holder_name}%")')
        if self.holder_change:
            self.conditions.append(f'(HOLDNUM_CHANGE_NAME="{self.holder_change}")')
        return "".join(self.conditions)

    def params(self) -> Dict:
        """
        :return:
        """
        params = {
            "filter": self.params_filter(),
            "sortColumns": "NOTICE_DATE,SECURITY_CODE,RANK",
            "sortTypes": "-1,1,1",
            "pageSize": self.size,
            "pageNumber": 1,
            "reportName": "RPT_DMSK_HOLDERS",
        }
        return self.base_param(params)
