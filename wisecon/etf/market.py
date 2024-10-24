from typing import Any, List, Dict, Callable, Optional
from wisecon.utils import time2int
from wisecon.types import BaseMapping, BaseRequestData


__all__ = [
    "ETFMarketMapping",
    "ETFMarket",
]


class ETFMarketMapping(BaseMapping):
    """"""
    market: Dict = {
        "MK0021": "",
        "MK0022": "",
        "MK0023": "",
        "MK0024": "",
        "MK0827": "",
    }
    columns: Dict = {
        "f1": "",
        "f2": "最新价",
        "f3": "涨跌幅",
        "f4": "涨跌额",
        "f5": "成交量",
        "f6": "成交额",
        "f7": "",
        "f8": "",
        "f9": "",
        "f10": "",
        "f12": "代码",
        "f13": "",
        "f14": "名称",
        "f15": "开盘价",
        "f16": "最低价",
        "f17": "最高价",
        "f18": "昨收",
        "f20": "",
        "f21": "",
        "f23": "",
        "f24": "",
        "f25": "",
        "f22": "",
        "f11": "",
        "f62": "",
        "f128": "",
        "f136": "",
        "f115": "",
        "f152": "",
    }


class ETFMarket(BaseRequestData):
    """ ERF Market """
    def __init__(
            self,
            market: Optional[List[str]] = None,
            sort_by: Optional[str] = "f3",
            limit: Optional[int] = 100,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        """"""
        self.market = market
        self.sort_by = sort_by
        self.limit = limit
        self.mapping = ETFMarketMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs
        self.request_set(description="ETF 市场")

    def base_url(self) -> str:
        """"""
        base_url = "https://push2.eastmoney.com/api/qt/clist/get"
        return base_url

    def _param_market(self):
        """"""
        if self.market is None:
            return "b:MK0021,b:MK0022,b:MK0023,b:MK0024,b:MK0827"
        elif isinstance(self.market, list):
            market = [f"b:{m}" for m in self.market if m in self.mapping.market]
            return ",".join(market)
        else:
            raise ValueError("market must be a list of market codes")

    def params(self) -> Dict:
        """
        :return:
        """
        params = {
            "pn": 1,
            "pz": self.limit,
            "po": 1,
            "np": 1,
            "fltt": 2,
            "invt": 2,
            "dect": 1,
            "wbp2u": "|0|0|0|web",
            "fid": self.sort_by,
            "fs": self._param_market(),
            "fields": ",".join(list(self.mapping.columns.keys())),
            "_": time2int(),
        }
        return params

    def clean_json(self, json_data: Optional[Dict]) -> List[Dict]:
        """"""
        response = json_data.get("data")
        data = response.pop("diff")
        self.metadata.response = response

        columns = self.mapping.filter_columns(columns=self.mapping.columns)

        def _clean_data(item):
            """"""
            return {k: v for k, v in item.items() if k in columns}

        data = list(map(_clean_data, data))
        return data
