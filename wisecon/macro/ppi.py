from typing import Any, Dict, Callable, Optional
from wisecon.types import BaseMapping
from .base import MacroRequestData


__all__ = [
    "PPIMapping",
    "PPI",
]


class PPIMapping(BaseMapping):
    """"""
    columns: Dict = {
        "REPORT_DATE": "报告日期",
        "TIME": "时间",
        "BASE": "当月",
        "BASE_SAME": "当月同比增长",
        "BASE_ACCUMULATE": "累计",
    }


class PPI(MacroRequestData):
    """中国 工业品出厂价格指数(PPI)"""
    def __init__(
            self,
            size: Optional[int] = 20,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        self.size = size
        self.mapping = PPIMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs
        self.request_set(
            response_type="json",
            description="中国 工业品出厂价格指数(PPI)",
        )

    def params(self) -> Dict:
        """
        :return:
        """
        columns = [
            "REPORT_DATE", "TIME", "BASE", "BASE_SAME", "BASE_ACCUMULATE"
        ]
        params = {
            "columns": ",".join(columns),
            "pageSize": self.size,
            "sortColumns": "REPORT_DATE",
            "sortTypes": "-1",
            "reportName": "RPT_ECONOMY_PPI",
        }
        return self.base_param(update=params)
