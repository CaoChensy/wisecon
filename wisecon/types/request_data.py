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
