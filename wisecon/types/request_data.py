import time
import requests
from requests import Response
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Literal
from wisecon.utils import headers, LoggerMixin
from .response_data import ResponseData, Metadata
from .mapping import BaseMapping


__all__ = [
    "assemble_url",
    "BaseRequestConfig",
    "BaseRequestData",
    "APICListRequestData",
    "APIStockFFlowDayLineRequestData",
    "APIUListNPRequestData",
    "APIDataV1RequestData",
    "APIStockKline",
    "APIStockKlineWithSSE",
]


def assemble_url(base_url: str, params: Dict) -> str:
    """"""
    query_string = '&'.join([f"{key}={value}" for key, value in params.items()])
    request_url = f"{base_url}?{query_string}"
    return request_url


class BaseRequestConfig(BaseModel):
    """"""
    mapping: Optional[Dict[str, str]] = Field(default=None)

    def _current_time(self) -> str:
        """"""
        return str(int(time.time() * 1E3))

    def params(self) -> Dict:
        """"""
        return dict()


class BaseRequestData(LoggerMixin):
    """"""
    query_config: Optional[BaseRequestConfig]
    headers: Optional[Dict]
    response_type: Literal["json", "text"]
    metadata: Optional[Metadata]
    mapping: Optional[BaseMapping]

    def request_set(
            self,
            _headers: Optional[Dict] = None,
            response_type: Optional[Literal["json", "text"]] = "json",
            description: Optional[str] = "",
            other_headers: Optional[Dict] = None
    ):
        """"""
        self.headers = _headers if _headers else headers
        self.response_type = response_type
        self.metadata = Metadata(description=description, columns=self.mapping.columns)
        if other_headers:
            self.headers.update(other_headers)

    def base_url(self) -> str:
        """"""
        return ""

    def params(self) -> Dict:
        """"""
        return dict()

    def request(self) -> Response:
        """"""
        base_url = self.base_url()
        params = self.params()
        self._logger(msg=f"URL: {assemble_url(base_url, params)}\n", color="green")
        response = requests.get(base_url, params=params, headers=self.headers)
        return response

    def request_json(self) -> Dict:
        """"""
        response = self.request()
        return response.json()

    def request_text(self) -> str:
        """"""
        response = self.request()
        return response.text

    def data(self, data: List[Dict], metadata: Optional[Metadata]) -> ResponseData:
        """"""
        return ResponseData(data=data, metadata=metadata)

    def clean_content(
            self,
            content: Optional[str],
    ) -> List[Dict]:
        return []

    def clean_json(
            self,
            json_data: Optional[Dict],
    ) -> List[Dict]:
        """"""
        return []

    def load(self) -> ResponseData:
        """"""
        if self.response_type == "text":
            content = self.request_text()
            data = self.clean_content(content)
        elif self.response_type == "json":
            json_data = self.request_json()
            data = self.clean_json(json_data)
        else:
            raise ValueError(f"Invalid response type: {self.response_type}")
        return self.data(data=data, metadata=self.metadata)


class APICListRequestData(BaseRequestData):
    """"""
    def base_url(self) -> str:
        return "https://push2.eastmoney.com/api/qt/clist/get"

    def clean_json(
            self,
            json_data: Optional[Dict],
    ) -> List[Dict]:
        """"""
        response = json_data.get("data", {})
        data = response.pop("diff")
        self.metadata.response = response
        return data


class APIStockFFlowDayLineRequestData(BaseRequestData):
    """"""
    def base_url(self) -> str:
        return "https://push2his.eastmoney.com/api/qt/stock/fflow/daykline/get"

    def clean_json(
            self,
            json_data: Optional[Dict],
    ) -> List[Dict]:
        """"""
        columns = list(self.mapping.columns.keys())
        response = json_data.get("data", {})
        data = response.pop("klines")
        data = [dict(zip(columns, item.split(","))) for item in data]
        self.metadata.response = response
        return data


class APIUListNPRequestData(BaseRequestData):
    """"""
    def base_url(self) -> str:
        return "https://push2.eastmoney.com/api/qt/ulist.np/get"

    def clean_json(
            self,
            json_data: Optional[Dict],
    ) -> List[Dict]:
        """"""
        response = json_data.get("data", {})
        data = response.pop("diff")
        self.metadata.response = response
        return data


class APIDataV1RequestData(BaseRequestData):
    """"""
    conditions: Optional[List[str]]
    security_code: Optional[str]
    start_date: Optional[str]
    end_date: Optional[str]
    date: Optional[str]

    def base_url(self) -> str:
        """"""
        return "https://datacenter-web.eastmoney.com/api/data/v1/get"

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


class APIStockKline(BaseRequestData):
    """"""
    def base_url(self) -> str:
        """"""
        return "https://push2his.eastmoney.com/api/qt/stock/kline/get"

    def clean_json(
            self,
            json_data: Optional[Dict],
    ) -> List[Dict]:
        response = json_data.get("data", {})
        data = response.pop("klines")
        self.metadata.response = response

        def trans_kline_data(line: str) -> Dict:
            """"""
            line_data = line.split(",")
            return dict(zip(list(self.mapping.columns.keys()), line_data))

        data = list(map(trans_kline_data, data))
        return data


class APIStockKlineWithSSE(BaseRequestData):
    """"""
    def base_url(self) -> str:
        """"""
        return "https://push2his.eastmoney.com/api/qt/stock/kline/get"

    def base_sse(self) -> str:
        """"""
        return "https://push2his.eastmoney.com/api/qt/stock/kline/sse"

    def clean_json(
            self,
            json_data: Optional[Dict],
    ) -> List[Dict]:
        """"""

        def clean_data(data: Dict) -> Dict:
            """"""
            columns = [
                "f11", "f13", "f15", "f17", "f19",
                "f31", "f33", "f35", "f37", "f39",
                "f191",
            ]
            for key, value in data.items():
                if key in columns:
                    data.update({key: value / 100})
            return data

        data = list(map(clean_data, [json_data.pop("data")]))
        self.metadata.response = json_data
        return data

# todo: 封装请求数据类
