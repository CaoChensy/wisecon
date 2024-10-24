from typing import Dict, Optional, List
from wisecon.types import BaseRequestData


__all__ = [
    "StockFormRequestData"
]


class StockFormRequestData(BaseRequestData):
    """"""
    conditions: Optional[List[str]]
    security_code: Optional[str]
    start_date: Optional[str]
    end_date: Optional[str]
    date: Optional[str]

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

    def filter_report_date(self, date_name: Optional[str] = "REPORT_DATE"):
        """"""
        if self.start_date:
            self.conditions.append(f"({date_name}>='{self.start_date}')")
        if self.end_date:
            self.conditions.append(f"({date_name}<='{self.end_date}')")
        if self.date:
            self.conditions.append(f"({date_name}='{self.date}')")

    def filter_security_code(self):
        """"""
        if self.security_code:
            self.conditions.append(f'(SECURITY_CODE="{self.security_code}")')

