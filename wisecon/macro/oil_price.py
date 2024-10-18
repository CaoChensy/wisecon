from typing import Any, Dict, Callable, Optional
from wisecon.types import BaseMapping
from .base import MacroRequestData


__all__ = [
    "OilPriceMapping",
    "OilPrice",
]


class OilPriceMapping(BaseMapping):
    """"""
    columns: Dict = {
        "DIM_DATE": "调整日期",
        "VALUE": "汽油价格(元/吨)",
        "CY_JG": "柴油价格(元/吨)",
        "QY_FD": "汽油涨跌",
        "CY_FD": "柴油涨跌",
    }


class OilPrice(MacroRequestData):
    """"""
    def __init__(
            self,
            size: Optional[int] = 20,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        self.size = size
        self.mapping = OilPriceMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs
        self.request_set(description="中国 汽柴油历史调价信息")
        
    def params(self) -> Dict:
        """
        :return:
        """
        columns = [
            "DIM_DATE", "VALUE", "CY_JG", "QY_FD", "CY_FD"
        ]
        params = {
            "columns": ",".join(columns),
            "pageSize": self.size,
            "sortColumns": "DIM_DATE",
            "sortTypes": "-1",
            "reportName": "RPTA_WEB_YJ_BD",
        }
        return self.base_param(update=params)
