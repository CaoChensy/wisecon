from typing import Any, Dict, Optional, Callable
from wisecon.types import APIDataV1RequestData, BaseMapping


__all__ = [
    "FundHolderListMapping",
    "FundHolderList",
]


class FundHolderListMapping(BaseMapping):
    """字段映射 基金持仓数据"""
    columns: Dict = {
        "SECUCODE": "证券代码",
        "SECURITY_CODE": "证券代码",
        "SECURITY_INNER_CODE": "证券内部代码",
        "SECURITY_NAME_ABBR": "证券简称",
        "REPORT_DATE": "报告日期",
        "HOLDER_CODE": "持有人代码",
        "HOLDER_NAME": "持有人名称",
        "PARENT_ORG_CODE": "母组织代码",
        "PARENT_ORGCODE_OLD": "旧母组织代码",
        "PARENT_ORG_NAME": "母组织名称",
        "ORG_TYPE_CODE": "组织类型代码",
        "ORG_TYPE": "组织类型",
        "TOTAL_SHARES": "总持股数",
        "HOLD_MARKET_CAP": "持有市值",
        "TOTAL_SHARES_RATIO": "总持股比例",
        "FREE_SHARES_RATIO": "自由流通股比例",
        "NETASSET_RATIO": "净资产比例",
        "ORG_NAME_ABBR": "组织名称简称"
    }


class FundHolderList(APIDataV1RequestData):
    """查询 依据基金代码查询基金持仓数据"""

    def __init__(
            self,
            holder_code: Optional[str] = None,
            date: Optional[str] = None,
            size: Optional[int] = 20,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        """
        Notes:
            ```python
            from wisecon.stock.main_holder import *

            data = FundHolderList(holder_code="516060", date="2024-09-30").load()
            data.to_frame(chinese_column=True)
            ```

        Args:
            holder_code: `持有组织代码/基金代码`
            date: 报告日期
            size: 数据条数
            verbose: 是否打印日志
            logger: 日志记录器
            **kwargs: 其他参数
        """
        self.holder_code = holder_code
        self.date = date
        self.size = size
        self.mapping = FundHolderListMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs
        self.request_set(description="基金持仓数据",)
        self.conditions = []
        self.validate_holder_code(code=holder_code)
        self.validate_date_is_end_if_quarter(date=date)

    def params_filter(self) -> str:
        """"""
        self.filter_report_date(date_name="REPORT_DATE")
        if self.holder_code:
            self.conditions.append(f'(HOLDER_CODE="{self.holder_code}")')
        else:
            raise
        return "".join(self.conditions)

    def params(self) -> Dict:
        """
        :return:
        """
        params = {
            "filter": self.params_filter(),
            "pageSize": self.size,
            "sortColumns": "SECURITY_CODE",
            "sortTypes": "-1",
            "reportName": "RPT_MAINDATA_MAIN_POSITIONDETAILS",
        }
        return self.base_param(update=params)
