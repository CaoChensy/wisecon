import time
import requests
from datetime import datetime
from requests import Response
from pydantic import BaseModel, Field
from typing import List, Dict, Union, Optional, Literal
from wisecon.utils import headers, LoggerMixin
from .response_data import ResponseData, Metadata
from .mapping import BaseMapping


__all__ = [
    "assemble_url",
    "BaseRequestConfig",
    "BaseRequestData",
    "ValidateParams",
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


class ValidateParams:
    """"""
    security_code: Union[str, List[str]]

    def validate_date_format(self, date: Union[str, List[str]], _format: str = "%Y-%m-%d"):
        """"""
        if isinstance(date, str):
            date = [date]
        for d in date:
            if isinstance(d, str):
                try:
                    datetime.strptime(d, _format)
                except ValueError:
                    raise ValueError(f"Invalid date format: {d}. Expected format: {_format}")

    def validate_date_is_end_if_quarter(self, date: str):
        """"""
        _format = "%Y-%m-%d"
        self.validate_date_format(date, _format=_format)
        date = datetime.strptime(date, _format)
        mark = [
            (date.month == 3 and date.day == 31),
            (date.month == 6 and date.day == 30),
            (date.month == 9 and date.day == 30),
            (date.month == 12 and date.day == 31),
        ]
        if not any(mark):
            raise ValueError(f"Date must be the last day of the quarter, your date: {date}")

    def validate_code(self, code: Union[str, List[str]], length: int = 6):
        """"""
        if isinstance(code, str):
            code = [code]
        mark = all([len(c) == 6 for c in code])
        if not mark:
            raise ValueError(f"Security code must be {length} characters.")

    def validate_holder_code(self, code: str):
        """"""
        self.validate_code(code)

    def validate_security_code(self, code: Union[str, List[str]]):
        """"""
        self.validate_code(code)

    def validate_max_security_codes(self, security_code: Union[str, List[str]]) -> None:
        """"""
        self.validate_code(code=security_code)
        if isinstance(security_code, list) and len(security_code) > 10:
            raise ValueError("security_code maximum length is 10.")

    def validate_size(self, size: int, max_size: int):
        """"""
        if size > max_size:
            raise ValueError(f"Size must be less than {max_size}, your size: {size}")

    def validate_params(self):
        """"""
        if hasattr(self, "security_code"):
            self.validate_security_code(self.security_code)
        if hasattr(self, "holder_code"):
            self.validate_holder_code(self.holder_code)


class BaseRequestData(LoggerMixin, ValidateParams):
    """"""
    query_config: Optional[BaseRequestConfig]
    headers: Optional[Dict]
    response_type: Literal["json", "text"]
    metadata: Optional[Metadata]
    mapping: Optional[BaseMapping]

    def request_set(
            self,
            _headers: Optional[Dict] = None,
            response_type: Optional[Literal["json", "text", "html"]] = "json",
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

    def params_drop_none(self, params: Dict) -> Dict:
        """"""
        return {k: v for k, v in params.items() if v is not None}

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

    def request_html(self) -> bytes:
        """"""
        response = self.request()
        return response.content

    def data(self, data: List[Dict], metadata: Optional[Metadata]) -> ResponseData:
        """"""
        return ResponseData(data=data, metadata=metadata)

    def clean_html(
            self,
            html: Optional[bytes],
    ) -> List[Dict]:
        return []

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
        elif self.response_type == "html":
            html = self.request_html()
            data = self.clean_html(html)
        elif self.response_type == "json":
            json_data = self.request_json()
            data = self.clean_json(json_data)
        else:
            raise ValueError(f"Invalid response type: {self.response_type}")
        return self.data(data=data, metadata=self.metadata)
