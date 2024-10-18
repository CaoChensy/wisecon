from typing import Any, Dict, Callable, Optional
from wisecon.types import BaseMapping
from .base import MacroRequestData


__all__ = [
    "GovIncomeMapping",
    "GovIncome",
]


class GovIncomeMapping(BaseMapping):
    """"""
    columns: Dict = {
        "START_DATE": "开始时间",
        "END_DATE": "截至时间",
        "BASE": "当月(亿元)",
        "BASE_SAME": "同比增长",
        "BASE_SEQUENTIAL": "环比增长",
        "BASE_ACCUMULATE": "累计(亿元)",
        "ACCUMULATE_SAME": "累计同比增长",
    }


class GovIncome(MacroRequestData):
    """"""
    def __init__(
            self,
            size: Optional[int] = 20,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        self.size = size
        self.mapping = GovIncomeMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs
        self.request_set(description="中国 财政收入（每年2月公布当年1-2月累计值）")

    def params(self) -> Dict:
        """
        :return:
        """
        columns = [
            "REPORT_DATE", "TIME", "BASE", "BASE_SAME", "BASE_SEQUENTIAL", "BASE_ACCUMULATE", "ACCUMULATE_SAME"
        ]
        params = {
            "columns": ",".join(columns),
            "pageSize": self.size,
            "sortColumns": "REPORT_DATE",
            "sortTypes": "-1",
            "reportName": "RPT_ECONOMY_INCOME",
        }
        return params
