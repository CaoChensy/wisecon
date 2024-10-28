from typing import Any, Dict, Optional, Callable
from wisecon.types import APIDataV1RequestData, BaseMapping


__all__ = [
    "StockHolderCollectMapping",
    "StockHolderCollect",
]


class StockHolderCollectMapping(BaseMapping):
    """字段映射 依据股票代码查询股票基金机构对该股票的汇总信息"""
    columns: Dict = {
        "SECURITY_INNER_CODE": "证券内部代码",
        "SECURITY_NAME_ABBR": "证券简称",
        "REPORT_DATE": "报告日期",
        "ORG_TYPE": "组织类型",
        "HOULD_NUM": "持有股数",
        "TOTAL_SHARES": "总股份数",
        "HOLD_VALUE": "持有市值",
        "FREESHARES_RATIO": "自由流通股比例",
        "HOLDCHA": "持仓变动",
        "HOLDCHA_NUM": "变动股数",
        "HOLDCHA_RATIO": "变动比例",
        "SECUCODE": "证券代码",
        "TOTALSHARES_RATIO": "总股份比例",
        "ORG_TYPE_NAME": "组织类型名称",
        "QCHANGE_RATE": "季度变动率",
        "FREE_MARKET_CAP": "自由流通市值",
        "FREE_SHARES": "自由流通股",
        "SECURITY_TYPE_CODE": "证券类型代码",
        "HOLDCHA_VALUE": "持仓变动市值",
        "SECURITY_CODE": "证券代码",
        "FREESHARES_RATIO_CHANGE": "自由流通股比例变动",
        "TYPE_NUM": "类型编号"
    }


class StockHolderCollect(APIDataV1RequestData):
    """查询 依据股票代码查询股票基金机构对该股票的汇总信息"""

    def __init__(
            self,
            security_code: Optional[str] = None,
            date: Optional[str] = None,
            size: Optional[int] = 8,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        """
        Notes:
            ```python
            from wisecon.stock.main_holder import *

            data = StockHolderCollect(security_code="002475", date="2024-09-30").load()
            data.to_frame(chinese_column=True)
            ```

        Args:
            security_code: 股票代码
            date: 报告日期
            size: 数据条数
            verbose: 是否打印日志
            logger: 日志记录器
            **kwargs: 其他参数
        """
        self.security_code = security_code
        self.date = date
        self.size = size
        self.mapping = StockHolderCollectMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs
        self.request_set(description="依据股票代码查询股票基金机构对该股票的汇总信息",)
        self.conditions = []
        self.validate_security_code(security_code)
        self.validate_date_is_end_if_quarter(date=date)

    def params_filter(self) -> str:
        """"""
        self.filter_report_date(date_name="REPORT_DATE")
        if self.security_code:
            self.conditions.append(f'(SECURITY_CODE="{self.security_code}")')
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
            "sortColumns": "",
            "sortTypes": "",
            "reportName": "RPT_MAIN_ORGHOLD",
        }
        return self.base_param(update=params)
