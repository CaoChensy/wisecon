import os
import time
import random
import requests
from requests import Response
from pydantic import BaseModel
from typing import List, Dict, Union, Literal, Optional
from wisecon.utils import tqdm_progress_bar
from wisecon.types.request_data import BaseRequestData, assemble_url
from wisecon.types.response_data import ResponseData


__all__ = [
    "TypeReport",
    "ReportData",
    "APIReportRequest",
]


TypeReport = Literal["个股研报", "行业研报", "策略报告", "宏观研究", "券商晨报"]


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
        if self.report_type is None or self.report_type == "*":
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

    def bytes_file(
            self,
            info_codes: List[str]
    ):
        """"""
        self.reports_data = []
        base_url = """https://pdf.dfcfw.com/pdf/H3_{}_1.pdf""".format
        for info_code in tqdm_progress_bar(info_codes):
            _report = ReportData(code=info_code)
            try:
                response = requests.get(base_url(info_code), headers=self.headers)
                _report.content = response.content
            except Exception as e:
                self._logger(msg=f"[{__class__.__name__}] Load `{info_code}` error, error message: {e}", color="red")
                _report.error = str(e)
            self.reports_data.append(_report)

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

    def save(
            self,
            path: str = "./reports",
            info_codes: Optional[List[str]] = None,
    ):
        """"""
        if not os.path.exists(path):
            os.makedirs(path)
        cache_path = os.path.join(path, "cache")
        if not os.path.exists(cache_path):
            os.makedirs(cache_path)
        pdf_path = cache_path = os.path.join(path, "pdf")
        if not os.path.exists(pdf_path):
            os.makedirs(pdf_path)

        if info_codes is None:
            response_data = self.load()
            if len(response_data.data) > 0:
                report_data = response_data.to_frame()
                info_codes = report_data["infoCode"].tolist()
                report_data.to_csv(os.path.join(cache_path, f"{str(int(time.time() * 1E3))}.csv"), index=False)
            else:
                info_codes = []
                self._logger(msg=f"[{__class__.__name__}] Not find report.")
        if len(info_codes) > 0:
            self.bytes_file(info_codes=info_codes)
            for _report in self.reports_data:
                if isinstance(_report.content, bytes):
                    file_path = os.path.join(pdf_path, f"{_report.code}.pdf")
                    with open(file_path, "wb") as f:
                        f.write(_report.content)
