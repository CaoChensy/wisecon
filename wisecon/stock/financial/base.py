from typing import Dict, Optional, List
from wisecon.types import APIDataV1RequestData
from wisecon.utils import time2int


__all__ = [
    "StockFormRequestData"
]


class StockFormRequestData(APIDataV1RequestData):
    """"""
    def base_param(self, update: Dict) -> Dict:
        """

        :param update:
        :return:
        """
        params = {
            "sortColumns": "PLAN_NOTICE_DATE",
            "sortTypes": -1,
            "pageSize": 50,
            "pageNumber": 1,
            "reportName": "RPT_SHAREBONUS_DET",
            "columns": "ALL",
            "quoteColumns": "",
            "source": "WEB",
            "client": "WEB",
        }
        params.update(update)
        return params
