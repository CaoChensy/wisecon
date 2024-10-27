from typing import Dict, Optional, List
from wisecon.types import APIDataV1RequestData


__all__ = [
    "StockFormRequestData"
]


class StockFormRequestData(APIDataV1RequestData):
    """"""
    conditions: Optional[List[str]]
    security_code: Optional[str]
    start_date: Optional[str]
    end_date: Optional[str]
    date: Optional[str]

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
            "source": "WEB",
            "client": "WEB",
        }
        params.update(update)
        return params
