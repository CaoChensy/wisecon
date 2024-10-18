from typing import Any, Dict, Callable, Optional
from wisecon.types import BaseMapping
from .base import MacroRequestData


__all__ = [
    "CurrencySupplyMapping",
    "CurrencySupply",
]


class CurrencySupplyMapping(BaseMapping):
    """"""

    columns: Dict = {
        "REPORT_DATE": "报告日期",
        "TIME": "时间",
        "BASIC_CURRENCY": "货币和准货币(M2)",
        "BASIC_CURRENCY_SAME": "M2-同比",
        "BASIC_CURRENCY_SEQUENTIAL": "M2-环比",
        "CURRENCY": "货币(M1)",
        "CURRENCY_SAME": "M1-同比",
        "CURRENCY_SEQUENTIAL": "M1-环比",
        "FREE_CASH": "流通中的现金(M0)",
        "FREE_CASH_SAME": "M0-同比",
        "FREE_CASH_SEQUENTIAL": "M0-环比",
    }


class CurrencySupply(MacroRequestData):
    """"""
    def __init__(
            self,
            size: Optional[int] = 20,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        self.size = size
        self.mapping = CurrencySupplyMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs
        self.request_set(
            response_type="json",
            description="中国 货币供应量",
        )

    def params(self) -> Dict:
        """
        :return:
        """
        columns = [
            "REPORT_DATE", "TIME", "BASIC_CURRENCY", "BASIC_CURRENCY_SAME", "BASIC_CURRENCY_SEQUENTIAL",
            "CURRENCY", "CURRENCY_SAME", "CURRENCY_SEQUENTIAL", "FREE_CASH", "FREE_CASH_SAME",
            "FREE_CASH_SEQUENTIAL"
        ]
        params = {
            "columns": ",".join(columns),
            "pageSize": self.size,
            "sortColumns": "REPORT_DATE",
            "sortTypes": "-1",
            "reportName": "RPT_ECONOMY_CURRENCY_SUPPLY",
        }
        return self.base_param(update=params)
