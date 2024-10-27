from typing import Any, Dict, Callable, Optional, List
from wisecon.types import BaseMapping, APIStockKlineWithSSE
from wisecon.types.columns import StockFeatures


__all__ = [
    "TickMapping",
    "Tick",
]


class TickMapping(BaseMapping):
    """字段映射 股票实时tick数据"""
    columns: Dict = StockFeatures().tick_columns()


class Tick(APIStockKlineWithSSE):
    """查询 股票实时tick数据"""
    def __init__(
            self,
            code: Optional[str] = None,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        """
        Notes:
            ```python
            from wisecon.stock.tick import Tick

            data = Tick(code="301618").load()
            print(data.to_frame(chinese_column=True))
            ```

        Args:
            code: 证券代码
            verbose: 是否打印日志
            logger: 日志打印函数
            **kwargs: 其他参数
        """
        self.code = code
        self.mapping = TickMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs
        self.request_set(description="股票实时tick数据")

    def params(self) -> Dict:
        """
        :return:
        """
        columns = [
            "f11", "f12", "f13", "f14", "f15", "f16", "f17", "f18", "f19", "f20",
            "f31", "f32", "f33", "f34", "f35", "f36", "f37", "f38", "f39", "f40",
            "f191", "f192", "f531",
        ]
        params = {
            "fields": ",".join(columns),
            "mpi": 1000,
            "invt": 2,
            "fltt": 1,
            "secid": f"0.{self.code}",
            "dect": 1,
            "wbp2u": "|0|0|0|web"
        }
        return params
