from typing import Any, Dict, Callable, Optional
from wisecon.types import BaseMapping
from .base import MacroRequestData


__all__ = [
    "CustomsMapping",
    "Customs",
]


class CustomsMapping(BaseMapping):
    """"""
    columns: Dict = {
        "REPORT_DATE": "报告日期",
        "TIME": "时间",
        "EXIT_BASE": "当月出口额（亿美金）",
        "IMPORT_BASE": "当月进口额（亿美金）",
        "EXIT_BASE_SAME": "当月出口额（同比）",
        "IMPORT_BASE_SAME": "当月进口额（同比）",
        "EXIT_BASE_SEQUENTIAL": "当月出口额（环比）",
        "IMPORT_BASE_SEQUENTIAL": "当月进口额（环比）",
        "EXIT_ACCUMULATE": "累计出口额（亿美金）",
        "IMPORT_ACCUMULATE": "累计进口额（亿美金）",
        "EXIT_ACCUMULATE_SAME": "累计出口额（同比）",
        "IMPORT_ACCUMULATE_SAME": "累计进口额（同比）",
    }


class Customs(MacroRequestData):
    """"""
    def __init__(
            self,
            size: Optional[int] = 20,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        self.size = size
        self.mapping = CustomsMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs
        self.request_set(
            response_type="json",
            description="中国 海关进出口增减情况一览表",
        )

    def params(self) -> Dict:
        """
        :return:
        """
        columns = [
            "REPORT_DATE", "TIME", "EXIT_BASE", "IMPORT_BASE", "EXIT_BASE_SAME", "IMPORT_BASE_SAME",
            "EXIT_BASE_SEQUENTIAL", "IMPORT_BASE_SEQUENTIAL", "EXIT_ACCUMULATE", "IMPORT_ACCUMULATE",
            "EXIT_ACCUMULATE_SAME", "IMPORT_ACCUMULATE_SAME"
        ]
        params = {
            "columns": ",".join(columns),
            "pageSize": self.size,
            "sortColumns": "REPORT_DATE",
            "sortTypes": "-1",
            "reportName": "RPT_ECONOMY_CUSTOMS",
        }
        return params
