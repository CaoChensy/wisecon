from typing import Any, Dict, Callable, Optional
from wisecon.types import BaseMapping
from .base import MacroRequestData


__all__ = [
    "TotalRetailMapping",
    "TotalRetail",
]


class TotalRetailMapping(BaseMapping):
    """"""
    columns: Dict = {
        "REPORT_DATE": "报告日期",
        "TIME": "时间",
        "RETAIL_TOTAL": "当月(亿元)",
        "RETAIL_TOTAL_SAME": "同比增长",
        "RETAIL_TOTAL_SEQUENTIAL": "环比增长",
        "RETAIL_TOTAL_ACCUMULATE": "累计(亿元)",
        "RETAIL_ACCUMULATE_SAME": "累计同比增长",
    }


class TotalRetail(MacroRequestData):
    """"""
    def __init__(
            self,
            size: Optional[int] = 20,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        self.size = size
        self.mapping = TotalRetailMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs
        self.request_set(description="中国 社会消费品零售总额 （每年2月公布当年1-2月累计值）")

    def params(self) -> Dict:
        """
        :return:
        """
        columns = [
            "REPORT_DATE", "TIME", "RETAIL_TOTAL", "RETAIL_TOTAL_SAME", "RETAIL_TOTAL_SEQUENTIAL",
            "RETAIL_TOTAL_ACCUMULATE", "RETAIL_ACCUMULATE_SAME"
        ]
        params = {
            "columns": ",".join(columns),
            "pageSize": self.size,
            "sortColumns": "REPORT_DATE",
            "sortTypes": "-1",
            "reportName": "RPT_ECONOMY_TOTAL_RETAIL",
        }
        return params
