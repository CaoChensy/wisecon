from typing import Any, Dict, Literal, Callable, Optional
from wisecon.types import BaseMapping, APIDataV1RequestData


__all__ = [
    "FreeHolderStockAnalysis",
    "FreeHolderStockAnalysisMapping",
]


class FreeHolderStockAnalysisMapping(BaseMapping):
    """字段映射 上市公司十大流通股东股东持股统计"""
    columns: Dict = {
        "COOPERATION_HOLDER_MARK": "合作股东标识",
        "END_DATE": "截止日期",
        "HOLDER_NAME": "股东名称",
        "HOLDER_TYPE": "股东类型",
        "HOLDNUM_CHANGE_TYPE": "持股变动类型",
        "STATISTICS_TIMES": "统计次数",
        "AVG_CHANGE_10TD": "10日平均变动",
        "MAX_CHANGE_10TD": "10日最大变动",
        "MIN_CHANGE_10TD": "10日最小变动",
        "AVG_CHANGE_30TD": "30日平均变动",
        "MAX_CHANGE_30TD": "30日最大变动",
        "MIN_CHANGE_30TD": "30日最小变动",
        "AVG_CHANGE_60TD": "60日平均变动",
        "MAX_CHANGE_60TD": "60日最大变动",
        "MIN_CHANGE_60TD": "60日最小变动",
        "SEAB_JOIN": "关联股票"
    }


class FreeHolderStockAnalysis(APIDataV1RequestData):
    """查询 上市公司十大流通股东股东持股统计"""
    def __init__(
            self,
            holder_name: Optional[str] = None,
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

            data = FreeHolderStockAnalysis(size=20, start_date="2024-09-30").load()
            data.to_frame(chinese_column=True)
            ```

        Args:
            holder_name: 股东名称
            holder_type: 股东类型 `["个人", "基金", "QFII", "社保", "券商", "信托"]`
            holder_change: 变动方向 `["新进", "增加", "不变", "减少"]`
            size: 返回条数
            start_date: 开始日期
            end_date: 结束日期
            date: 指定日期
            verbose: 是否显示日志
            logger: 自定义日志
            **kwargs: 其他参数
        """
        self.holder_name = holder_name
        self.holder_type = holder_type
        self.holder_change = holder_change
        self.size = size
        self.start_date = start_date
        self.end_date = end_date
        self.date = date
        self.mapping = FreeHolderStockAnalysisMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs
        self.request_set(response_type="json", description="上市公司十大流通股东股东持股统计")
        self.conditions = []

    def params_hold_change(self):
        """"""
        change_mapping = {"新进": "002", "增加": "003", "不变": "004", "减少": "005"}
        if self.holder_change:
            return change_mapping.get(self.holder_change, "001")
        else:
            return "001"

    def params_filter(self) -> str:
        """"""
        self.filter_report_date(date_name="END_DATE")
        if self.holder_type:
            self.conditions.append(f'(HOLDER_TYPE="{self.holder_type}")')
        if self.holder_change:
            self.conditions.append(f'(HOLDNUM_CHANGE_TYPE="{self.params_hold_change()}")')
        if self.holder_name:
            self.conditions.append(f'(HOLDER_NAME+like+"%{self.holder_name}%")')
        return "".join(self.conditions)

    def params(self) -> Dict:
        """
        :return:
        """
        params = {
            "filter": self.params_filter(),
            "sortColumns": "STATISTICS_TIMES,COOPERATION_HOLDER_MARK",
            "sortTypes": "-1,-1",
            "pageSize": self.size,
            "pageNumber": 1,
            "reportName": "RPT_COOPFREEHOLDERS_ANALYSISNEW",
        }
        return self.base_param(params)
