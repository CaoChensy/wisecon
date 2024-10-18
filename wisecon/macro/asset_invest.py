from typing import Any, Dict, Callable, Optional
from wisecon.types import BaseMapping
from .base import MacroRequestData


__all__ = [
    "AssetInvestMapping",
    "AssetInvest",
]


class AssetInvestMapping(BaseMapping):
    """"""
    columns: Dict = {
        "REPORT_DATE": "报告日期",
        "TIME": "时间",
        "BASE": "当月(亿元)",
        "BASE_SAME": "同比增长",
        "BASE_SEQUENTIAL": "环比增长",
        "BASE_ACCUMULATE": "自年初累计(亿元)",
    }


class AssetInvest(MacroRequestData):
    """"""
    def __init__(
            self,
            size: Optional[int] = 20,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        self.size = size
        self.mapping = AssetInvestMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs
        self.request_set(
            response_type="json",
            description="中国 城镇固定资产投资",
        )

    def params(self) -> Dict:
        """
        :return:
        """
        columns = [
            "REPORT_DATE", "TIME", "BASE", "BASE_SAME", "BASE_SEQUENTIAL", "BASE_ACCUMULATE"
        ]
        params = {
            "columns": ",".join(columns),
            "pageSize": self.size,
            "sortColumns": "REPORT_DATE",
            "sortTypes": "-1",
            "reportName": "RPT_ECONOMY_ASSET_INVEST",
        }
        return self.base_param(update=params)
