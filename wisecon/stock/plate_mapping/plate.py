from typing import Any, Dict, Literal, Callable, Optional
from wisecon.types import APICListMapping, APICListRequestData


__all__ = [
    "PlateCodeMapping",
    "PlateCode",
]


class PlateCodeMapping(APICListMapping):
    """字段映射 行业、概念、地区编码数据"""


class PlateCode(APICListRequestData):
    """查询 行业、概念、地区编码数据"""
    def __init__(
            self,
            plate_type: Optional[Literal["行业", "概念", "地区"]] = None,
            size: Optional[int] = 500,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        """
        Notes:
            ```python
            from wisecon.stock.capital_flow import *

            # 1. 查询有哪些概念板块
            data = PlateCode(plate_type="概念").load()
            data.to_frame(chinese_column=True)

            # 2. 查询有哪些地区板块
            data = PlateCode(plate_type="地区").load()
            data.to_frame(chinese_column=True)

            # 3. 查询有哪些行业板块
            data = PlateCode(plate_type="行业").load()
            data.to_frame(chinese_column=True)
            ```

        Args:
            plate_type: 板块类型, `["行业", "概念", "地区"]`
            size: 返回数据量
            verbose: 是否打印日志
            logger: 自定义日志函数
            **kwargs: 其他参数
        """
        self.plate_type = plate_type
        self.size = size
        self.mapping = PlateCodeMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs
        self.request_set(description="行业、概念、地区编码数据", )

    def params_plate_type(self) -> str:
        """"""
        plate_mapping = {
            "行业": "m:90+t:2",
            "概念": "m:90+t:3",
            "地区": "m:90+t:1",
        }
        if self.plate_type in plate_mapping:
            return plate_mapping[self.plate_type]
        else:
            return plate_mapping["行业"]

    def params(self) -> Dict:
        """"""
        params = {
            "fid": "f62",
            "po": 1,
            "pz": self.size,
            "pn": 1,
            "np": 1,
            "fs": self.params_plate_type(),
            "fields": "f12,f13,f14,f62",
        }
        return params
