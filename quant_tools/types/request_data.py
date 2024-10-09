import time
import requests
from pydantic import BaseModel, Field
from typing import Dict, Optional
from quant_tools.utils import headers, LoggerMixin


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

    def to_params(self) -> Dict:
        """"""
        return dict()


class BaseRequestData(LoggerMixin):
    """"""
    query_config: Optional[BaseRequestConfig]

    def _base_url(self) -> str:
        """"""
        return ""

    def request_json(self) -> Dict:
        """"""
        base_url = self._base_url()
        if hasattr(self, "query_config"):
            params = self.query_config.to_params()
        elif hasattr(self, "to_params"):
            params = self.to_params()
        else:
            raise AttributeError("No query_config or to_params found.")
        response = requests.get(base_url, params=params, headers=headers)
        data = response.json()
        if data.get("success") is False:
            url = assemble_url(base_url, params)
            raise ValueError(f"Request failed: {url}")
        return data
