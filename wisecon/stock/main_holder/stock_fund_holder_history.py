from typing import Any, Dict, Optional, Callable
from wisecon.types import APIDataV1RequestData, BaseMapping


__all__ = [
    "StockFundHolderHistoryMapping",
    "StockFundHolderHistory",
]


class StockFundHolderHistoryMapping(BaseMapping):
    """字段映射 依据股票代码查询股票基金机构对该股票的持仓历史"""
    columns: Dict = {
        "SECUCODE": "证券代码",
        "SECURITY_CODE": "证券代码",
        "SECURITY_INNER_CODE": "证券内部代码",
        "SECURITY_NAME_ABBR": "证券简称",
        "REPORT_DATE": "报告日期",
        "OTAL_SHARES": "总股份数",
        "HOLD_MARKET_CAP": "持有市值",
        "TOTAL_SHARES_RATIO": "总股份比例",
        "FREE_SHARES_RATIO": "自由流通股比例",
        "CHANGE_SHARES": "变动股数",
        "CHANGE_SHARES_RATIO": "变动比例"
    }


class StockFundHolderHistory(APIDataV1RequestData):
    """查询 依据股票代码查询股票基金机构对该股票的持仓历史"""

    def __init__(
            self,
            security_code: Optional[str] = None,
            start_date: Optional[str] = '2015-09-30',
            size: Optional[int] = 20,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        """
        Notes:
            ```python
            from wisecon.stock.main_holder import *

            data = StockFundHolderHistory(security_code="002475").load()
            data.to_frame(chinese_column=True)
            ```

        Args:
            security_code: 股票代码
            start_date: 报告日期
            size: 数据条数
            verbose: 是否打印日志
            logger: 日志记录器
            **kwargs: 其他参数
        """
        self.security_code = security_code
        self.start_date = start_date
        self.size = size
        self.mapping = StockFundHolderHistoryMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs
        self.request_set(description="依据股票代码查询股票基金机构对该股票的持仓历史",)
        self.conditions = []
        self.validate_security_code(code=security_code)
        self.validate_date_is_end_if_quarter(date=start_date)

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
            "sortColumns": "REPORT_DATE",
            "sortTypes": "-1",
            "reportName": "RPT_MAINDATA_CHANGE_POSITION",
        }
        return self.base_param(update=params)
