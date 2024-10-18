from typing import Any, Dict, Callable, Optional
from wisecon.types import BaseMapping
from .base import MacroRequestData


__all__ = [
    "FDIMapping",
    "FDI",
]


class FDIMapping(BaseMapping):
    """"""
    columns: Dict = {
        "REPORT_DATE": "报告日期",
        "TIME": "时间",
        "ACTUAL_FOREIGN": "当月(亿美元)",
        "ACTUAL_FOREIGN_SAME": "同比增长",
        "ACTUAL_FOREIGN_SEQUENTIAL": "环比增长",
        "ACTUAL_FOREIGN_ACCUMULATE": "累计(亿美元)",
        "FOREIGN_ACCUMULATE_SAME": "同比增长",
    }


class FDI(MacroRequestData):
    """中国 外商直接投资数据(FDI)"""
    def __init__(
            self,
            size: Optional[int] = 20,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        self.size = size
        self.mapping = FDIMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs
        self.request_set(description="中国 外商直接投资数据(FDI)")

    def params(self) -> Dict:
        """
        :return:
        """
        columns = [
            "REPORT_DATE", "TIME", "ACTUAL_FOREIGN", "ACTUAL_FOREIGN_SAME",
            "ACTUAL_FOREIGN_SEQUENTIAL", "ACTUAL_FOREIGN_ACCUMULATE", "FOREIGN_ACCUMULATE_SAME"
        ]
        params = {
            "columns": ",".join(columns),
            "pageSize": self.size,
            "sortColumns": "REPORT_DATE",
            "sortTypes": "-1",
            "reportName": "RPT_ECONOMY_FDI",
        }
        return self.base_param(update=params)
