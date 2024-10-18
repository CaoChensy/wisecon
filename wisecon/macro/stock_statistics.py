from typing import Any, Dict, Callable, Optional
from wisecon.types import BaseMapping
from .base import MacroRequestData


__all__ = [
    "StockStatisticsMapping",
    "StockStatistics",
]


class StockStatisticsMapping(BaseMapping):
    """"""
    columns: Dict = {
        "REPORT_DATE": "报告日期",
        "TIME": "时间",
        "TOTAL_SHARES_SH": "发行总股本(SH)",
        "TOTAL_MARKE_SH": "市价总值(SH)",
        "DEAL_AMOUNT_SH": "成交金额(SH)",
        "VOLUME_SH": "成交量(SH)",
        "HIGH_INDEX_SH": "A股最高综合股价指数(SH)",
        "LOW_INDEX_SH": "A股最低综合股价指数(SH)",
        "TOTAL_SZARES_SZ": "发行总股本(SZ)",
        "TOTAL_MARKE_SZ": "市价总值(SZ)",
        "DEAL_AMOUNT_SZ": "成交金额(SZ)",
        "VOLUME_SZ": "成交量(SZ)",
        "HIGH_INDEX_SZ": "A股最高综合股价指数(SZ)",
        "LOW_INDEX_SZ": "A股最低综合股价指数(SZ)",
    }
    
    
class StockStatistics(MacroRequestData):
    """"""
    def __init__(
            self,
            size: Optional[int] = 20,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        self.size = size
        self.mapping = StockStatisticsMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs
        self.request_set(description="中国 全国股票交易统计表")
    
    def params(self) -> Dict:
        """
        :return:
        """
        columns = [
            "REPORT_DATE", "TIME", "TOTAL_SHARES_SH", "TOTAL_MARKE_SH", "DEAL_AMOUNT_SH", "VOLUME_SH",
            "HIGH_INDEX_SH", "LOW_INDEX_SH", "TOTAL_SZARES_SZ", "TOTAL_MARKE_SZ", "DEAL_AMOUNT_SZ",
            "VOLUME_SZ", "HIGH_INDEX_SZ", "LOW_INDEX_SZ"
        ]
        params = {
            "columns": ",".join(columns),
            "pageSize": self.size,
            "sortColumns": "REPORT_DATE",
            "sortTypes": "-1",
            "reportName": "RPT_ECONOMY_STOCK_STATISTICS",
        }
        return self.base_param(update=params)
