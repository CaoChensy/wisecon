from typing import Any, Dict, Callable, Optional
from wisecon.types import BaseMapping
from .base import MacroRequestData


__all__ = [
    "GoodsIndexMapping",
    "GoodsIndex",
]


class GoodsIndexMapping(BaseMapping):
    """"""
    columns: Dict = {
        "REPORT_DATE": "报告日期",
        "TIME": "时间",
        "BASE": "总指数",
        "BASE_SAME": "总指数（同比）",
        "BASE_SEQUENTIAL": "总指数（环比）",
        "FARM_BASE": "农产品",
        "FARM_BASE_SAME": "农产品（同比）",
        "FARM_BASE_SEQUENTIAL": "农产品（环比）",
        "MINERAL_BASE": "矿产品",
        "MINERAL_BASE_SAME": "矿产品（同比）",
        "MINERAL_BASE_SEQUENTIAL": "矿产品（环比）",
        "ENERGY_BASE": "煤油电",
        "ENERGY_BASE_SAME": "煤油电（同比）",
        "ENERGY_BASE_SEQUENTIAL": "煤油电（环比）",
    }


class GoodsIndex(MacroRequestData):
    """"""
    def __init__(
            self,
            size: Optional[int] = 20,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        self.size = size
        self.mapping = GoodsIndexMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs
        self.request_set(description="中国 企业商品价格指数")

    def params(self) -> Dict:
        """
        :return:
        """
        columns = [
            "REPORT_DATE", "TIME", "BASE", "BASE_SAME", "BASE_SEQUENTIAL", "FARM_BASE", "FARM_BASE_SAME",
            "FARM_BASE_SEQUENTIAL", "MINERAL_BASE", "MINERAL_BASE_SAME", "MINERAL_BASE_SEQUENTIAL", "ENERGY_BASE",
            "ENERGY_BASE_SAME", "ENERGY_BASE_SEQUENTIAL"
        ]
        params = {
            "columns": ",".join(columns),
            "pageSize": self.size,
            "sortColumns": "REPORT_DATE",
            "sortTypes": "-1",
            "reportName": "RPT_ECONOMY_GOODS_INDEX",
        }
        return self.base_param(update=params)
