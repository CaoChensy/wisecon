from typing import Any, Dict, Optional, Literal, Callable
from wisecon.types import APIDataV1RequestData, BaseMapping


__all__ = [
    "DepartmentActiveMapping",
    "DepartmentActive",
]


class DepartmentActiveMapping(BaseMapping):
    """字段映射 每日活跃营业部"""
    columns: Dict = {
        "OPERATEDEPT_NAME": "营业部名称",
        "ONLIST_DATE": "上榜日期",
        "BUYER_APPEAR_NUM": "买方出现次数",
        "SELLER_APPEAR_NUM": "卖方出现次数",
        "TOTAL_BUYAMT": "总买入金额",
        "TOTAL_SELLAMT": "总卖出金额",
        "TOTAL_NETAMT": "净金额",
        "BUY_STOCK": "买入股票",
        "OPERATEDEPT_CODE": "营业部代码",
        "SECURITY_NAME_ABBR": "证券简称",
        "OPERATEDEPT_CODE_OLD": "旧营业部代码",
        "ORG_NAME_ABBR": "组织名称简称"
    }


class DepartmentActive(APIDataV1RequestData):
    """查询 每日活跃营业部"""

    def __init__(
            self,
            start_date: Optional[str] = None,
            end_date: Optional[str] = None,
            date: Optional[str] = None,
            size: Optional[int] = 20,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        """
        Notes:
            ```python
            from wisecon.stock.ranking import *

            data = DepartmentActive(date="2024-10-28").load()
            data.to_frame(chinese_column=True)
            ```

        Args:
            start_date: 开始日期, 格式: yyyy-MM-dd, 默认值: None
            end_date: 结束日期, 格式: yyyy-MM-dd, 默认值: None
            date: 日期, 格式: yyyy-MM-dd, 默认值: None
            size: 数据条数
            verbose: 是否打印日志
            logger: 日志记录器
            **kwargs: 其他参数
        """
        self.start_date = start_date
        self.end_date = end_date
        self.date = date
        self.size = size
        self.mapping = DepartmentActiveMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs
        self.request_set(description="每日活跃营业部",)
        self.conditions = []
        self.validate_date_format(date=[date, start_date, end_date])

    def params_filter(self) -> str:
        """"""
        self.filter_report_date(date_name="ONLIST_DATE")
        return "".join(self.conditions)

    def params(self) -> Dict:
        """
        :return:
        """
        params = {
            "filter": self.params_filter(),
            "pageSize": self.size,
            "sortColumns": "TOTAL_NETAMT,ONLIST_DATE,OPERATEDEPT_CODE",
            "sortTypes": "-1,-1,1",
            "reportName": "RPT_OPERATEDEPT_ACTIVE",
        }
        return self.base_param(update=params)
