import os
import time
import requests
from typing import Any, List, Dict, Literal, Optional, Callable
from wisecon.types import BaseMapping, APIAnnouncement, ReportData
from wisecon.utils import tqdm_progress_bar
from lumix.documents import StructuredPDF


__all__ = [
    "Announcement",
]


class AnnouncementMapping(BaseMapping):
    """"""
    columns: Dict = {
        "art_code": "公告代码",
        "codes": "股票代码信息",
        "columns": "栏目信息",
        "display_time": "显示时间",
        "eiTime": "EI时间",
        "language": "语言",
        "listing_state": "上市状态",
        "notice_date": "公告日期",
        "product_code": "产品代码",
        "sort_date": "排序日期",
        "source_type": "来源类型",
        "title": "标题",
        "title_ch": "中文标题",
        "title_en": "英文标题"
    }


class Announcement(APIAnnouncement):
    """"""
    def __init__(
            self,
            node_name: Literal["不限公告", "财务报告", "融资公告", "风险提示", "信息变更", "重大事项", "资产重组", "持股变动",],
            date: Optional[str],
            security_code: Optional[str] = None,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        """

        Args:
            node_name:
            date: yyyy-MM-dd
            security_code:
            verbose:
            logger:
            **kwargs:
        """
        self.node_name = node_name
        self.date = date
        self.security_code = security_code
        self.mapping = AnnouncementMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs
        self.request_set(response_type="json", description="公告信息")

    def f_node_type(self, node_name: Optional[str] = None) -> int:
        """"""
        node_type = {
            "不限公告": 0,
            "财务报告": 1,
            "融资公告": 2,
            "风险提示": 3,
            "信息变更": 4,
            "重大事项": 5,
            "资产重组": 6,
            "持股变动": 7,
        }
        return node_type.get(node_name, 0)

    def params(self) -> Dict:
        """"""
        params = {
            "page_index": 1,
            "page_size": 50,
            "f_node": self.f_node_type(self.node_name)
        }
        if self.security_code is not None:
            params.update({
                "ann_type": "A",
                "stock_list": self.security_code,
            })
        else:
            params.update({
                "ann_type": "SHA,CYB,SZA,BJA,INV",
            })
        return self.base_param(update=params)

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

    def to_bytes_content(self, info_code: str, tool: Literal["request", "scrapy", "httpx", "selenium"] = "request") -> bytes:
        """"""
        base_url = f"""https://pdf.dfcfw.com/pdf/H2_{info_code}_1.pdf"""
        try:
            if tool == "request":
                self._logger(msg=f"[{__class__.__name__}] Use: {tool}")
                response = requests.get(base_url, headers=self.headers)
                return response.content
            elif tool == "scrapy":
                from wisecon.utils.fetch_pdf import fetch_pdf_bytes
                self._logger(msg=f"[{__class__.__name__}] Use: {tool}")
                response = fetch_pdf_bytes(base_url, headers=self.headers)
                return response
            elif tool == "httpx":
                import httpx
                with httpx.Client(headers=self.headers, http2=False) as client:
                    response = client.get(base_url, headers=self.headers)
                return response.content
            elif tool == "selenium":
                from wisecon.utils.fetch_pdf import fetch_pdf_bytes_use_selenium
                return fetch_pdf_bytes_use_selenium(base_url)

        except Exception as e:
            msg = f"[{__class__.__name__}] Load `{info_code}` error, error message: {e}"
            self._logger(msg=msg, color="red")
            raise Exception(msg)

    def to_text(self, info_code: str, tool: Literal["request", "scrapy", "httpx", "selenium"] = "request") -> str:
        """"""
        bytes_data = self.to_bytes_content(info_code=info_code, tool=tool)
        pdf = StructuredPDF(path_or_data=bytes_data)
        return pdf.to_text()

    def save_pdf(self, info_code: str, path: Optional[str] = None, tool: Literal["request", "scrapy", "httpx", "selenium"] = "request"):
        """"""
        if path is None:
            path = f"{info_code}.pdf"
        bytes_data = self.to_bytes_content(info_code=info_code, tool=tool)
        with open(path, "wb") as f:
            f.write(bytes_data)

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
