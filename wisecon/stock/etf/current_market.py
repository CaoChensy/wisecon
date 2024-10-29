from typing import Any, Dict, Callable, Optional, Literal
from wisecon.types import BaseMapping, APICListRequestData


__all__ = [
    "ETFCurrentMarketMapping",
    "ETFCurrentMarket",
]


class ETFCurrentMarketMapping(BaseMapping):
    """字段映射 ETF/LOF当前市场行情"""
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


class ETFCurrentMarket(APICListRequestData):
    """查询 ETF/LOF当前市场行情"""
    def __init__(
            self,
            market: Literal["ETF", "LOF", "封闭基金"] = "ETF",
            sort_by: Optional[str] = "f3",
            size: Optional[int] = 100,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        """
        Notes:
            ```python
            # 查询ETF市场当前行情
            data = ETFCurrentMarket(market="ETF", verbose=True).load()
            data.to_frame(chinese_column=True)

            # 查询LOF市场当前行情
            data = ETFCurrentMarket(market="LOF", verbose=True).load()
            data.to_frame(chinese_column=True)

            # 查询封闭基金当前行情
            data = ETFCurrentMarket(market="封闭基金", verbose=True).load()
            data.to_frame(chinese_column=True)
            ```

        Args:
            market: 市场类型
            sort_by: 排序字段
            size: 返回数据量
            verbose: 是否打印日志
            logger: 自定义日志打印函数
            **kwargs: 其他参数
        """
        self.market = market
        self.sort_by = sort_by
        self.size = size
        self.mapping = ETFCurrentMarketMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs
        self.request_set(description="ETF/LOF当前市场行情")

    def params_market(self) -> str:
        """"""
        market_mapping = {
            "ETF": "b:MK0021,b:MK0022,b:MK0023,b:MK0024,b:MK0827",
            "LOF": "b:MK0404,b:MK0405,b:MK0406,b:MK0407",
            "封闭基金": "e:19",
        }
        return market_mapping[self.market]

    def params(self) -> Dict:
        """"""
        params = {
            "pz": self.size,
            "fid": self.sort_by,
            "fs": self.params_market(),
            "fields": ",".join(list(self.mapping.columns.keys())),
        }
        return self.base_param(update=params)
