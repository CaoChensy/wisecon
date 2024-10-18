from typing import Any, Dict, Callable, Optional
from wisecon.types import BaseMapping
from .base import MacroRequestData


__all__ = [
    "FaithIndexMapping",
    "FaithIndex",
]


class FaithIndexMapping(BaseMapping):
    """"""
    columns: Dict = {
        "REPORT_DATE": "报告日期",
        "TIME": "时间",
        "CONSUMERS_FAITH_INDEX": "消费者信心指数",
        "FAITH_INDEX_SAME": "消费者信心指数（同比）",
        "FAITH_INDEX_SEQUENTIAL": "消费者信心指数（环比）",
        "CONSUMERS_ASTIS_INDEX": "消费者满意指数",
        "ASTIS_INDEX_SAME": "消费者满意指数（同比）",
        "ASTIS_INDEX_SEQUENTIAL": "消费者满意指数（环比）",
        "CONSUMERS_EXPECT_INDEX": "消费者预期指数",
        "EXPECT_INDEX_SAME": "消费者预期指数（同比）",
        "EXPECT_INDEX_SEQUENTIAL": "消费者预期指数（环比）",
    }


class FaithIndex(MacroRequestData):
    """"""
    def __init__(
            self,
            size: Optional[int] = 20,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        self.size = size
        self.mapping = FaithIndexMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs
        self.request_set(description="中国 消费者信心指数")

    def params(self) -> Dict:
        """
        :return:
        """
        columns = [
            "REPORT_DATE", "TIME", "CONSUMERS_FAITH_INDEX", "FAITH_INDEX_SAME", "FAITH_INDEX_SEQUENTIAL",
            "CONSUMERS_ASTIS_INDEX", "ASTIS_INDEX_SAME", "ASTIS_INDEX_SEQUENTIAL", "CONSUMERS_EXPECT_INDEX",
            "EXPECT_INDEX_SAME", "EXPECT_INDEX_SEQUENTIAL"
        ]
        params = {
            "columns": ",".join(columns),
            "pageSize": self.size,
            "sortColumns": "REPORT_DATE",
            "sortTypes": "-1",
            "reportName": "RPT_ECONOMY_FAITH_INDEX",
        }
        return self.base_param(update=params)
