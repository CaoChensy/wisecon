from typing import Any, Dict, Callable, Optional
from wisecon.types import BaseMapping
from .base import MacroRequestData


__all__ = [
    "StockOpenMapping",
    "StockOpen",
]


class StockOpenMapping(BaseMapping):
    """"""
    columns: Dict = {
        "STATISTICS_DATE": "数据日期",
        "ADD_INVESTOR": "新增投资者(万户)",
        "ADD_INVESTOR_QOQ": "新增投资者(环比)",
        "ADD_INVESTOR_YOY": "新增投资者(同比)",
        "END_INVESTOR": "期末投资者(万户)",
        "END_INVESTOR_A": "期末投资者(A股)",
        "END_INVESTOR_B": "期末投资者(B股)",
        "CLOSE_PRICE": "上证指数(收盘)",
        "CHANGE_RATE": "上证指数(涨跌幅)",
        "TOTAL_MARKET_CAP": "沪深总市值",
        "AVERAGE_MARKET_CAP": "沪深户均市值",
        "STATISTICS_DATE_NY": "月份"
    }


class StockOpen(MacroRequestData):
    """"""
    def __init__(
            self,
            size: Optional[int] = 20,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        self.size = size
        self.mapping = StockOpenMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs
        self.request_set(
            response_type="json",
            description="中国 股票账户统计详细数据",
        )

    def params(self) -> Dict:
        """
        :return:
        """
        columns = [
            "STATISTICS_DATE", "ADD_INVESTOR", "ADD_INVESTOR_QOQ", "ADD_INVESTOR_YOY", "END_INVESTOR",
            "END_INVESTOR_A", "END_INVESTOR_B", "CLOSE_PRICE", "CHANGE_RATE", "TOTAL_MARKET_CAP",
            "AVERAGE_MARKET_CAP", "STATISTICS_DATE_NY",
        ]
        params = {
            "columns": ",".join(columns),
            "pageSize": self.size,
            "sortColumns": "STATISTICS_DATE",
            "sortTypes": "-1",
            "reportName": "RPT_STOCK_OPEN_DATA",
        }
        return self.base_param(update=params)
