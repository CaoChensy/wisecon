from typing import Any, List, Dict, Callable, Optional, Literal
from wisecon.types import BaseMapping, ResponseData, BaseRequestData


__all__ = [
    "MarketValuationMapping",
    "MarketValuation",
]


TypeMarketCode = Literal["000300", "000001", "000688", "399001", "399006",]


class MarketValuationMapping(BaseMapping):
    """"""
    market: Dict = {
        "000300": "沪深两市",
        "000001": "沪市主板",
        "000688": "科创板",
        "399001": "深市主板",
        "399006": "创业板",
    }
    columns: Dict = {
        "TRADE_MARKET_CODE": "市场代码",
        "TRADE_DATE": "交易日期",
        "CLOSE_PRICE": "指数",
        "CHANGE_RATE": "涨跌幅(%)",
        "SECURITY_INNER_CODE": "",
        "LISTING_ORG_NUM": "个股总数",
        "TOTAL_SHARES": "总股本(股)",
        "FREE_SHARES": "流通股本(股)",
        "TOTAL_MARKET_CAP": "总市值(元)",
        "FREE_MARKET_CAP": "流通市值(元)",
        "PE_TTM_AVG": "平均市盈率(PE-TTM)"
    }
    close_price: Dict = {
        "000300": "沪深300",
        "000001": "上证指数",
        "000688": "科创50",
        "399001": "深证指数",
        "399006": "创业板指数",
    }


class MarketValuation(BaseRequestData):
    """ ERF Market """
    def __init__(
            self,
            market: Optional[TypeMarketCode] = "000300",
            start_date: Optional[str] = "2020-10-08",
            end_date: Optional[str] = None,
            limit: Optional[int] = 50,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        """"""
        self.market = market
        self.start_date = start_date
        self.end_date = end_date
        self.limit = limit
        self.mapping = MarketValuationMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs

    def _base_url(self) -> str:
        """"""
        base_url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
        return base_url

    def _param_filter(self) -> str:
        """"""
        if self.market not in self.mapping.market:
            raise ValueError(f"market {self.market} not in {self.mapping.market}")
        condition = []
        if self.start_date:
            condition.append(f"(TRADE_DATE>='{self.start_date}')")
        if self.end_date:
            condition.append(f"(TRADE_DATE<='{self.end_date}')")
        if self.market:
            condition.append(f"(TRADE_MARKET_CODE=\"{self.market}\")")
        return "".join(condition)

    def params(self) -> Dict:
        """"""
        params = {
            "sortColumns": "TRADE_DATE",
            "sortTypes": -1,
            "pageSize": self.limit,
            "pageNumber": 1,
            "reportName": "RPT_VALUEMARKET",
            "columns": "ALL",
            "quoteColumns": "",
            "filter": self._param_filter(),
            "source": "WEB",
            "client": "WEB",
        }
        return params

    def clean_data(self, data) -> List[Dict]:
        """"""
        columns = self.mapping.filter_columns(columns=self.mapping.columns)

        def _clean_data(item):
            """"""
            return {k: v for k, v in item.items() if k in columns}

        data = list(map(_clean_data, data))
        return data

    def load_data(self) -> ResponseData:
        """
        :return:
        """
        metadata = self.request_json().get("result", {})
        data = metadata.pop("data")
        data = self.clean_data(data=data)
        self.update_metadata(metadata)
        return ResponseData(data=data, metadata=metadata)

    def update_metadata(self, metadata: Dict):
        """"""
        columns = self.mapping.filter_columns(columns=self.mapping.columns)
        columns.update({"CLOSE_PRICE": self.mapping.close_price.get(self.market)})
        metadata.update({
            "description": "市场估值",
            "columns": columns,
        })
