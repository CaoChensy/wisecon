import time
import random
import requests
from pydantic import BaseModel
from typing import List, Dict, Union, Literal, Optional
from wisecon.types.request_data import BaseRequestData, assemble_url
from wisecon.types.response_data import ResponseData


__all__ = [
    "TypeReport",
    "ReportData",
    "APIReportRequest",
]


TypeReport = Literal["个股研报", "行业研报", "策略报告", "宏观研究", "券商晨报", "不限类型"]


class ReportData(BaseModel):
    """"""
    code: str
    content: Optional[bytes] = None
    error: Optional[str] = None


class APIReportRequest(BaseRequestData):
    """"""
    page_no: int
    reports_data: List[ReportData]
    q_type: Optional[Union[int, str]] = None
    report_type: Optional[TypeReport] = "*"

    def reports_type(self):
        """"""
        report_types = ["个股研报", "行业研报", "策略报告", "宏观研究", "券商晨报"]
        if self.report_type is None or self.report_type == "不限类型":
            self.q_type = "*"
        elif self.report_type in report_types:
            self.q_type = report_types.index(self.report_type)

    def base_url(self) -> str:
        """jg/dg/list"""
        url = "https://reportapi.eastmoney.com/report/"
        if self.q_type is None:
            self.reports_type()
        if self.q_type in [0, 1,]:
            url += "list"
        else:
            url += "dg"
        return url

    def base_param(self, update: Dict) -> Dict:
        """"""
        params = {}
        params.update(update)
        return params

    def random_cb(self) -> str:
        """"""
        return str(int(random.random() * 1E7 + 1))

    def current_time(self) -> str:
        """"""
        return str(int(time.time() * 1E3))

    def data_page(self):
        """"""
        base_url = self.base_url()
        params = self.params()
        self._logger(msg=f"[URL] {assemble_url(base_url, params)}\n", color="green")
        response = requests.get(base_url, params=params, headers=self.headers)
        json_data = response.json()
        total_page = json_data.get("TotalPage")
        page_no = json_data.get("pageNo")
        return json_data, total_page, page_no

    def request(self) -> List[Dict]:
        """"""
        json_data, total_page, page_no = self.data_page()
        data = json_data.pop("data")
        self.metadata.response = json_data
        while page_no < total_page:
            self.page_no += 1
            json_data, total_page, page_no = self.data_page()
            page_data = json_data.pop("data")
            data.extend(page_data)
            self.metadata.response = json_data
        return data

    def load(self) -> ResponseData:
        """"""
        return self.data(data=self.request(), metadata=self.metadata)
