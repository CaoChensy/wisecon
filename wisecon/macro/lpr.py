from typing import Any, Dict, Callable, Optional
from wisecon.types import BaseMapping
from .base import MacroRequestData


__all__ = [
    "LPRMapping",
    "LPR",
]


class LPRMapping(BaseMapping):
    """"""
    columns: Dict = {
        "TRADE_DATE": "日期",
        "LPR1Y": "LPR_1Y利率(%)",
        "LPR5Y": "LPR_5Y利率(%)",
        "RATE_1": "短期贷款利率:6个月至1年(含)(%)",
        "RATE_2": "中长期贷款利率:5年以上(%)",
    }


class LPR(MacroRequestData):
    """"""
    def __init__(
            self,
            size: Optional[int] = 20,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        self.size = size
        self.mapping = LPRMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs
        self.request_set(
            response_type="json",
            description="中国 LPR品种详细数据",
        )

    def params(self) -> Dict:
        """
        :return:
        """
        columns = [
            "TRADE_DATE", "LPR1Y", "LPR5Y", "RATE_1", "RATE_2"
        ]
        params = {
            "columns": ",".join(columns),
            "pageSize": self.size,
            "sortColumns": "TRADE_DATE",
            "sortTypes": "-1",
            "reportName": "RPTA_WEB_RATE",
        }
        return self.base_param(update=params)
