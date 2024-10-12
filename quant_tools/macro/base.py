from typing import Dict, Optional, List
from quant_tools.types import BaseRequestData
from quant_tools.utils import time2int


__all__ = [
    "MacroRequestData"
]


class MacroRequestData(BaseRequestData):
    """"""

    def base_url(self) -> str:
        """"""
        base_url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
        return base_url

    def base_param(self, update: Dict) -> Dict:
        """"""
        params = {
            "pageNumber": "1",
            "source": "WEB",
            "client": "WEB",
            "_": time2int(),
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
