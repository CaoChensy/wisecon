from typing import Any, Dict, Callable, Optional
from wisecon.types import BaseMapping
from .base import MacroRequestData


__all__ = [
    "PMIMapping",
    "PMI",
]


class PMIMapping(BaseMapping):
    """"""
    columns: Dict = {
        "REPORT_DATE": "报告日期",
        "TIME": "时间",
        "MAKE_INDEX": "制造业指数",
        "MAKE_SAME": "制造业同比增长",
        "NMAKE_INDEX": "非制造业指数",
        "NMAKE_SAME": "非制造业同比增长",
    }


class PMI(MacroRequestData):
    """采购经理人指数(PMI)"""
    def __init__(
            self,
            size: Optional[int] = 20,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        self.size = size
        self.verbose = verbose
        self.mapping = PMIMapping()
        self.logger = logger
        self.kwargs = kwargs
        self.request_set(
            response_type="json",
            description="中国 采购经理人指数(PMI)",
        )

    def params(self) -> Dict:
        """"""
        columns = [
            "REPORT_DATE", "TIME", "MAKE_INDEX", "MAKE_SAME", "NMAKE_INDEX",
            "NMAKE_SAME"
        ]
        params = {
            "columns": ",".join(columns),
            "pageSize": self.size,
            "sortColumns": "REPORT_DATE",
            "sortTypes": "-1",
            "reportName": "RPT_ECONOMY_PMI",
        }
        return self.base_param(update=params)
