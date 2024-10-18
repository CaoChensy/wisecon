from typing import Any, Dict, Callable, Optional
from wisecon.types import BaseMapping
from .base import MacroRequestData


__all__ = [
    "GoldCurrencyMapping",
    "GoldCurrency",
]


class GoldCurrencyMapping(BaseMapping):
    """"""
    columns: Dict = {
        "REPORT_DATE": "报告日期",
        "TIME": "时间",
        "GOLD_RESERVES": "黄金储备(亿美元)",
        "GOLD_RESERVES_SAME": "黄金储备(同比)",
        "GOLD_RESERVES_SEQUENTIAL": "黄金储备(环比)",
        "FOREX": "国家外汇储备(亿美元)",
        "FOREX_SAME": "国家外汇储备(同比)",
        "FOREX_SEQUENTIAL": "国家外汇储备(环比)",
    }


class GoldCurrency(MacroRequestData):
    """"""
    def __init__(
            self,
            size: Optional[int] = 20,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        self.size = size
        self.mapping = GoldCurrencyMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs
        self.request_set(description="中国 外汇和黄金储备")

    def params(self) -> Dict:
        """
        :return:
        """
        columns = [
            "REPORT_DATE", "TIME", "GOLD_RESERVES", "GOLD_RESERVES_SAME", "GOLD_RESERVES_SEQUENTIAL",
            "FOREX", "FOREX_SAME", "FOREX_SEQUENTIAL"
        ]
        params = {
            "columns": ",".join(columns),
            "pageSize": self.size,
            "sortColumns": "REPORT_DATE",
            "sortTypes": "-1",
            "reportName": "RPT_ECONOMY_GOLD_CURRENCY",
        }
        return self.base_param(update=params)
