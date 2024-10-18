from typing import Any, Dict, Callable, Optional
from wisecon.types import ResponseData, BaseMapping
from .base import MacroRequestData


__all__ = [
    "BoomIndexMapping",
    "BoomIndex",
]


class BoomIndexMapping(BaseMapping):
    """"""
    columns: Dict = {
        "REPORT_DATE": "报告日期",
        "TIME": "时间",
        "BOOM_INDEX": "企业景气指数",
        "FAITH_INDEX": "企业家信心指数",
        "BOOM_INDEX_SAME": "企业景气指数（同比）",
        "BOOM_INDEX_SEQUENTIAL": "企业景气指数（环比）",
        "FAITH_INDEX_SAME": "企业家信心指数（同比）",
        "FAITH_INDEX_SEQUENTIAL": "企业家信心指数（环比）",
    }


class BoomIndex(MacroRequestData):
    """"""
    def __init__(
            self,
            size: Optional[int] = 20,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        self.size = size
        self.mapping = BoomIndexMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs
        self.request_set(response_type="json", description="中国 企业景气及企业家信心指数")

    def params(self) -> Dict:
        """
        :return:
        """
        columns = [
            "REPORT_DATE", "TIME", "BOOM_INDEX", "FAITH_INDEX", "BOOM_INDEX_SAME",
            "BOOM_INDEX_SEQUENTIAL", "FAITH_INDEX_SAME", "FAITH_INDEX_SEQUENTIAL"
        ]
        params = {
            "columns": ",".join(columns),
            "pageSize": self.size,
            "sortColumns": "REPORT_DATE",
            "sortTypes": "-1",
            "reportName": "RPT_ECONOMY_BOOM_INDEX",
        }
        return self.base_param(params)
