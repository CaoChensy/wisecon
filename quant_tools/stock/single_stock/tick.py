from pydantic import Field
from typing import Any, Dict, Callable, Optional
from quant_tools.types import BaseRequestConfig, ResponseData, BaseRequestData
from quant_tools.types.columns import StockFeatures
from .base import url


__all__ = [
    "TickQueryConfig",
    "Tick",
]


class TickQueryConfig(BaseRequestConfig):
    """"""
    code: Optional[str] = Field(default=None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def params(self) -> Dict:
        """
        :return:
        """
        features = StockFeatures()
        self.mapping = features.tick_columns()
        params = {
            "fields": ",".join(list(self.mapping.keys())),
            "mpi": 1000,
            "invt": 2,
            "fltt": 1,
            "secid": f"0.{self.code}",
            "dect": 1,
            "wbp2u": "|0|0|0|web"
        }
        return params


class Tick(BaseRequestData):
    """"""
    def __init__(
            self,
            query_config: Optional[TickQueryConfig] = None,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        if query_config is None:
            self.query_config = TickQueryConfig.model_validate(kwargs)
        else:
            self.query_config = query_config
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs

    def _base_url(self) -> str:
        """"""
        return url.signal_stock_get

    def clean_data(self, data: Dict) -> Dict:
        """"""
        columns = [
            "f11", "f13", "f15", "f17", "f19",
            "f31", "f33", "f35", "f37", "f39",
            "f191",
        ]
        for key, value in data.items():
            if key in columns:
                data.update({key: value / 100})
        return data

    def load_data(self) -> ResponseData:
        """
        :return:
        """
        metadata = self.request_json()
        data = list(map(self.clean_data, [metadata.pop("data")]))
        self.update_metadata(metadata)
        return ResponseData(data=data, metadata=metadata)

    def update_metadata(self, metadata: Dict):
        """"""
        metadata.update({
            "description": "股票 tick数据",
            "columns": self.query_config.mapping
        })
