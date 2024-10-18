from typing import Any, Dict, Callable, Optional
from wisecon.types import BaseMapping
from .base import MacroRequestData


__all__ = [
    "IndusGrowMapping",
    "IndusGrow",
]


class IndusGrowMapping(BaseMapping):
    """"""
    columns: Dict = {
        "REPORT_DATE": "报告日期",
        "TIME": "时间",
        "BASE_SAME": "同比增长",
        "BASE_ACCUMULATE": "累计增长",
    }


class IndusGrow(MacroRequestData):
    """"""
    def __init__(
            self,
            size: Optional[int] = 20,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        self.size = size
        self.mapping = IndusGrowMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs
        self.request_set(description="中国 工业增加值增长 （每年2月公布当年1-2月累计值）")

    def params(self) -> Dict:
        """
        :return:
        """
        columns = [
            "REPORT_DATE", "TIME", "BASE_SAME", "BASE_ACCUMULATE"
        ]
        params = {
            "columns": ",".join(columns),
            "pageSize": self.size,
            "sortColumns": "REPORT_DATE",
            "sortTypes": "-1",
            "reportName": "RPT_ECONOMY_INDUS_GROW",
        }
        return self.base_param(update=params)
