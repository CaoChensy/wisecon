from pydantic import Field
from typing import Any, Dict, Literal, Callable, Optional
from quant_tools.types import ResponseData, BaseRequestData, BaseRequestConfig


__all__ = [
    "MarketCapitalFlowQueryConfig",
    "MarketCapitalFlow",
]


TypeMarketCode = Literal["000001", "399001", "399006", "000003", "399003"]


class MarketCapitalFlowQueryConfig(BaseRequestConfig):
    """"""
    code: Optional[TypeMarketCode] = Field(default="000001")
    size: Optional[int] = Field(default=0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def params(self) -> Dict:
        """
        :return:
        """
        params = {
            "lmt": self.size,
            "klt": 101,
            "fields1": "f1,f2,f3,f7",
            "fields2": "f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61,f62,f63,f64,f65",
            "secid": f"0.{self.code}",
            "_": self._current_time(),
        }
        return params


class MarketCapitalFlow(BaseRequestData):
    """"""
    def __init__(
            self,
            query_config: Optional[MarketCapitalFlowQueryConfig] = None,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        """
        :param code:
            "000001": 沪市, "399001": 深市, "399006": 创业板, "000003": 沪B, "399003": 深B
        :param query_config:
        :param verbose:
        :param logger:
        :param kwargs:
        """
        if query_config is None:
            self.query_config = MarketCapitalFlowQueryConfig.model_validate(kwargs)
        else:
            self.query_config = query_config
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs

    def _base_url(self) -> str:
        """"""
        base_url = "https://push2his.eastmoney.com/api/qt/stock/fflow/daykline/get"
        return base_url

    def load_data(self) -> ResponseData:
        """
        :return:
        """
        metadata = self.request_json().get("data", {})
        data = metadata.pop("klines")
        data = [item.split(",") for item in data]
        self.update_metadata(metadata)
        self._logger(msg=f"[{__class__.__name__}] Find {len(data)} reports.", color="green")
        return ResponseData(data=data, metadata=metadata)

    def update_metadata(self, metadata: Dict):
        """"""
        metadata.update({
            "description": "大盘资金流向历史数据(沪深两市)",
            "columns": [
                "日期", "主力净流入净额", "小单净流入净额", "中单净流入净额", "大单净流入净额",
                "超大单净流入净额", "主力净流入净占比", "小单净流入净占比", "中单净流入净占比",
                "大单净流入净占比", "超大单净流入净占比", "收盘价", "涨跌幅", "a", "b"
            ],
            "columns_mapping": {
                "f1": "日期",
                "f2": "主力净流入净额",
                "f3": "小单净流入净额",
                "f7": "中单净流入净额",
                "f51": "大单净流入净额",
                "f52": "超大单净流入净额",
                "f53": "主力净流入净占比",
                "f54": "小单净流入净占比",
                "f55": "中单净流入净占比",
                "f56": "大单净流入净占比",
                "f57": "超大单净流入净占比",
                "f58": "上证收盘价",
                "f59": "上证涨跌幅",
                "f60": "深证收盘价",
                "f61": "深证涨跌幅",
                "f62": "",
                "f63": "",
                "f64": "",
                "f65": "",
            }
        })
