from typing import Any, Dict, Callable, Optional, Literal
from wisecon.types import APIDataV1RequestData, BaseMapping


__all__ = [
    "MarketValuationMapping",
    "MarketValuation",
]


class MarketValuationMapping(BaseMapping):
    """字段映射 市场整体估值"""
    columns: Dict = {
        "TRADE_MARKET_CODE": "市场代码",
        "TRADE_DATE": "交易日期",
        "CLOSE_PRICE": "指数值",
        "CHANGE_RATE": "涨跌幅(%)",
        "SECURITY_INNER_CODE": "内部代码",
        "LISTING_ORG_NUM": "个股总数",
        "TOTAL_SHARES": "总股本(股)",
        "FREE_SHARES": "流通股本(股)",
        "TOTAL_MARKET_CAP": "总市值(元)",
        "FREE_MARKET_CAP": "流通市值(元)",
        "PE_TTM_AVG": "平均市盈率(PE-TTM)"
    }


class MarketValuation(APIDataV1RequestData):
    """查询 市场整体估值
    ```json
    {
        "000300": "沪深300",
        "000001": "上证指数",
        "000688": "科创50",
        "399001": "深证指数",
        "399006": "创业板指数",
    }
    ```
    """
    def __init__(
            self,
            market: Optional[Literal["沪深两市", "沪市主板", "科创板", "深市主板", "创业板",]] = "沪深两市",
            start_date: Optional[str] = "2020-10-08",
            end_date: Optional[str] = None,
            size: Optional[int] = 50,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        """
        Notes:
            ```python
            data = MarketValuation(market=market, size=5).load()
            data.to_frame(chinese_column=True)
            ```

        Args:
            market: 市场名称
            start_date: 开始日期
            end_date: 结束日期
            size: 返回条数
            verbose: 是否显示日志
            logger: 自定义日志
            **kwargs: 其他参数
        """
        self.market = market
        self.start_date = start_date
        self.end_date = end_date
        self.size = size
        self.mapping = MarketValuationMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs
        self.request_set(description="市场整体估值")
        self.conditions = []
        self.validate_date_format(date=[start_date, end_date], )

    def params_market(self):
        """"""
        market_mapping = {
            "沪深两市": "000300",
            "沪市主板": "000001",
            "科创板": "000688",
            "深市主板": "399001",
            "创业板": "399006",
        }
        self.conditions.append(f"(TRADE_MARKET_CODE=\"{market_mapping[self.market]}\")")

    def params_filter(self) -> str:
        """"""
        self.filter_report_date(date_name="TRADE_DATE")
        self.params_market()
        return "".join(self.conditions)

    def params(self) -> Dict:
        """"""
        params = {
            "sortColumns": "TRADE_DATE",
            "sortTypes": -1,
            "pageSize": self.size,
            "reportName": "RPT_VALUEMARKET",
            "filter": self.params_filter(),
        }
        return self.base_param(update=params)
