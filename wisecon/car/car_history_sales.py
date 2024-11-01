from typing import Any, Dict, Callable, Optional, Literal
from wisecon.types import BaseMapping, APICarHistoryRequestData


__all__ = [
    "CarHistorySalesMapping",
    "CarHistorySales",
]


class CarHistorySalesMapping(BaseMapping):
    """字段映射 汽车历史销量"""
    columns: Dict = {}


class CarHistorySales(APICarHistoryRequestData):
    """查询 汽车历史销量"""
    def __init__(
            self,
            data_type: Literal["汽车销量"] = "汽车销量",
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        """
        Notes:
            ```python
            data = CarHistorySales(data_type="电动车销量",).load()
            data.to_frame(chinese_column=True)
            ```

        Args:
            data_type: 查询类型
            verbose: 是否打印日志
            logger: 自定义日志打印函数
            **kwargs: 其他参数
        """
        self.data_type = data_type
        self.mapping = CarHistorySalesMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs
        self.request_set(description="汽车历史销量", response_type="html")
        self.data_mark = self.params_data_mark()
        self.params_multi_pages()

    def params_data_mark(self) -> str:
        """"""
        data_mark_mapping = {
            "汽车销量": "month",
            "品牌销量": "brand",
        }
        return data_mark_mapping[self.data_type]

    def params_multi_pages(self):
        if self.data_type in ["汽车销量", "品牌销量"]:
            self.multi_pages = True
        else:
            self.multi_pages = False
