from typing import Any, Dict, Callable, Optional
from wisecon.types import BaseMapping
from .base import MacroRequestData


__all__ = [
    "TaxMapping",
    "Tax",
]


class TaxMapping(BaseMapping):
    """"""
    columns: Dict = {
        "START_DATE": "开始时间",
        "END_DATE": "截至时间",
        "TAX_INCOME": "税收收入合计(亿元)",
        "TAX_INCOME_SAME": "较上年同期(%)",
        "TAX_INCOME_SEQUENTIAL": "季度环比(%)",
    }

    
class Tax(MacroRequestData):
    """"""
    def __init__(
            self,
            size: Optional[int] = 20,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        self.size = size
        self.mapping = TaxMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs
        self.request_set(description="中国 全国税收收入")
    
    def params(self) -> Dict:
        """
        :return:
        """
        columns = [
            "REPORT_DATE", "TIME", "TAX_INCOME", "TAX_INCOME_SAME", "TAX_INCOME_SEQUENTIAL"
        ]
        params = {
            "columns": ",".join(columns),
            "pageSize": self.size,
            "sortColumns": "REPORT_DATE",
            "sortTypes": "-1",
            "reportName": "RPT_ECONOMY_TAX",
        }
        return self.base_param(update=params)
