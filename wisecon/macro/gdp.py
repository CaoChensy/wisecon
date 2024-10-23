from typing import Any, Dict, Callable, Optional
from wisecon.types import BaseMapping
from .base import MacroRequestData


__all__ = [
    "GDPMapping",
    "GDP",
]


class GDPMapping(BaseMapping):
    """字段映射 GDP"""
    columns: Dict = {
        "REPORT_DATE": "报告日期",
        "TIME": "时间",
        "DOMESTICL_PRODUCT_BASE": "国内生产总值",
        "FIRST_PRODUCT_BASE": "第一产业绝对值（亿元）",
        "SECOND_PRODUCT_BASE": "第二产业绝对值（亿元）",
        "THIRD_PRODUCT_BASE": "第三产业绝对值（亿元）",
        "SUM_SAME": "国内生产总值同比增长",
        "FIRST_SAME": "第一产业同比增长",
        "SECOND_SAME": "第二产业同比增长",
        "THIRD_SAME": "第三产业同比增长",
    }


class GDP(MacroRequestData):
    """查询 GDP（中国）"""
    def __init__(
            self,
            size: Optional[int] = 20,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        """
        Args:
            size: 最大数据量
            verbose: 是否打印日志
            logger: 自定义日志
            **kwargs: 其他参数

        Examples:
            >>> from wisecon.macro import GDP
            >>> data = GDP(size=20).load()
            >>> data.to_frame(chinese_column=True)
        """
        self.size = size
        self.mapping = GDPMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs
        self.request_set(description="中国 国内生产总值(GDP)")

    def params(self) -> Dict:
        """"""
        columns = [
            "REPORT_DATE", "TIME", "DOMESTICL_PRODUCT_BASE", "FIRST_PRODUCT_BASE",
            "SECOND_PRODUCT_BASE", "THIRD_PRODUCT_BASE", "SUM_SAME", "FIRST_SAME",
            "SECOND_SAME", "THIRD_SAME"
        ]
        params = {
            "columns": ",".join(columns),
            "pageSize": self.size,
            "sortColumns": "REPORT_DATE",
            "sortTypes": "-1",
            "reportName": "RPT_ECONOMY_GDP",
        }
        return params
