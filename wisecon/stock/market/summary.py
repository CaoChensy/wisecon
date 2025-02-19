from typing import Any, Dict, Callable, Optional, Annotated
from wisecon.types import BaseMapping, APIMarketSummary


__all__ = [
    "LastDayMarketSummaryMapping",
    "LastDayMarketSummary",
]


class LastDayMarketSummaryMapping(BaseMapping):
    """字段映射 市场总貌"""
    columns: Dict = {
        "nt": "市场名称",
        "td": "交易日期",
        "v": "成交量",
        "tv": "成交金额",
        "ts": "总市值",
        "ns": "新股数量",
        "cn": "公司数量",
        "ttm": "市盈率(TTM)"
    }


class LastDayMarketSummary(APIMarketSummary):
    """查询 查询昨日市场（深市、沪市、创业板）总体交易数据"""
    def __init__(
            self,
            verbose: Annotated[Optional[bool], "", False] = False,
            logger: Annotated[Optional[Callable], "", False] = None,
            **kwargs: Annotated[Any, "", False],
    ):
        """
        Notes:
            ```python
            from wisecon.stock.market import *

            # 市场总貌：查询昨日市场（深市、沪市、创业板）总体交易数据
            data = LastDayMarketSummary().load()
            data.to_frame(chinese_column=True)
            ```

        Args:
            verbose: 是否打印日志
            logger: 自定义日志打印函数
            **kwargs: 其他参数
        """
        self.mapping = LastDayMarketSummaryMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs
        self.request_set(description="市场总貌")

    def params(self) -> Dict:
        """"""
        return {}
