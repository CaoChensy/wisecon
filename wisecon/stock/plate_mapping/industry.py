from typing import Any, Dict, Callable, Optional
from wisecon.types import BaseMapping, APIDataV1RequestData


__all__ = [
    "IndustryCodeMapping",
    "IndustryCode",
]


class IndustryCodeMapping(BaseMapping):
    """字段映射 行业编码数据"""
    columns: Dict = {
        "INDUSTRY_CODE": "行业编码",
        "INDUSTRY_NAME": "行业名称",
    }


class IndustryCode(APIDataV1RequestData):
    """查询 行业编码数据"""
    def __init__(
            self,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        """
        Notes:
            ```python
            from wisecon.stock.plate_mapping import *

            # 1. 查询有哪些行业编码
            data = IndustryCode().load()
            data.to_frame(chinese_column=True)
            ```

        Args:
            verbose: 是否打印日志
            logger: 自定义日志函数
            **kwargs: 其他参数
        """
        self.mapping = IndustryCodeMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs
        self.request_set(description="行业编码数据", )

    def params(self) -> Dict:
        """"""
        params = {
            "reportName": "RPT_INDUSTRY_SW2021",
            "sortColumns": "INDUSTRY_CODE",
            "sortTypes": 1
        }
        return self.base_param(update=params)
