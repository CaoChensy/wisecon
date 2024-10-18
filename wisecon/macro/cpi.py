from typing import Any, Dict, Callable, Optional
from wisecon.types import BaseMapping
from .base import MacroRequestData


__all__ = [
    "CPIMapping",
    "CPI",
]


class CPIMapping(BaseMapping):
    """"""
    columns: Dict = {
        "REPORT_DATE": "报告日期",
        "TIME": "时间",
        "NATIONAL_SAME": "全国同期",
        "NATIONAL_BASE": "全国基期",
        "NATIONAL_SEQUENTIAL": "全国环比",
        "NATIONAL_ACCUMULATE": "全国累计",
        "CITY_SAME": "城市同期",
        "CITY_BASE": "城市基期",
        "CITY_SEQUENTIAL": "城市环比",
        "CITY_ACCUMULATE": "城市累计",
        "RURAL_SAME": "农村同期",
        "RURAL_BASE": "农村基期",
        "RURAL_SEQUENTIAL": "农村环比",
        "RURAL_ACCUMULATE": "农村累计",
    }


class CPI(MacroRequestData):
    """"""
    def __init__(
            self,
            size: Optional[int] = 20,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        self.size = size
        self.mapping = CPIMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs
        self.request_set(
            response_type="json",
            description="中国 居民消费价格指数(CPI，上年同月=100)",
        )

    def params(self) -> Dict:
        """"""
        columns = [
            "REPORT_DATE", "TIME", "NATIONAL_SAME", "NATIONAL_BASE", "NATIONAL_SEQUENTIAL",
            "NATIONAL_ACCUMULATE", "CITY_SAME", "CITY_BASE", "CITY_SEQUENTIAL", "CITY_ACCUMULATE",
            "RURAL_SAME", "RURAL_BASE", "RURAL_SEQUENTIAL", "RURAL_ACCUMULATE",
        ]
        params = {
            "columns": ",".join(columns),
            "pageSize": self.size,
            "sortColumns": "REPORT_DATE",
            "sortTypes": "-1",
            "reportName": "RPT_ECONOMY_CPI",
        }
        return self.base_param(update=params)
