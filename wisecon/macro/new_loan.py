from typing import Any, Dict, Callable, Optional
from wisecon.types import BaseMapping
from .base import MacroRequestData


__all__ = [
    "NewLoanQueryConfig",
    "NewLoan",
]


class NewLoanQueryConfig(BaseMapping):
    """"""
    columns: Dict = {
        "REPORT_DATE": "报告日期",
        "TIME": "时间",
        "RMB_LOAN": "当月(亿元)",
        "RMB_LOAN_SAME": "同比增长",
        "RMB_LOAN_SEQUENTIAL": "环比增长",
        "RMB_LOAN_ACCUMULATE": "累计(亿元)",
        "LOAN_ACCUMULATE_SAME": "同比增长",
    }


class NewLoan(MacroRequestData):
    """"""
    def __init__(
            self,
            size: Optional[int] = 20,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        self.size = size
        self.mapping = NewLoanQueryConfig()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs
        self.request_set(description="中国 新增信贷数据")

    def params(self) -> Dict:
        """
        :return:
        """
        columns = [
            "REPORT_DATE", "TIME", "RMB_LOAN", "RMB_LOAN_SAME", "RMB_LOAN_SEQUENTIAL",
            "RMB_LOAN_ACCUMULATE", "LOAN_ACCUMULATE_SAME"
        ]
        params = {
            "columns": ",".join(columns),
            "pageSize": self.size,
            "sortColumns": "REPORT_DATE",
            "sortTypes": "-1",
            "reportName": "RPT_ECONOMY_RMB_LOAN",
        }
        return self.base_param(update=params)
