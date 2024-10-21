from typing import Dict, Optional, List
from wisecon.types import BaseRequestData
from wisecon.utils import time2int


__all__ = [
    "StockFormRequestData"
]


class StockFormRequestData(BaseRequestData):
    """"""

    def base_url(self) -> str:
        """"""
        base_url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
        return base_url

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

    def clean_json(
            self,
            json_data: Optional[Dict],
    ) -> List[Dict]:
        """"""
        response = json_data.get("result", {})
        data = response.pop("data")
        self.metadata.response = response
        return data
