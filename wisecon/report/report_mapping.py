import time
import requests
import pandas as pd
from typing import Dict
from wisecon.utils import LoggerMixin
from wisecon.types.headers import headers
from wisecon.types import ResponseData


__all__ = [
    "ConceptionMap"
]


class ConceptionMap(LoggerMixin):
    """"""
    base_url: str = "https://reportapi.eastmoney.com/report/bk"
    mapping_code: Dict[str, str] = {
        "地域板块": "020",
        "行业板块": "016",
        "概念板块": "007",
    }

    def __init__(self):
        """"""
        self.map_industry = self.list_industry()
        self.map_conception = self.list_conception()
        self.map_district = self.list_district()
        self.mapping_data = sum([
            self.map_conception.data, self.map_industry.data, self.map_district.data
        ], [])

    def _get_data(self, params: Dict) -> ResponseData:
        """"""
        response = requests.get(self.base_url, params=params, headers=headers.headers)
        metadata = response.json()
        data = metadata.pop("data")
        return ResponseData(data=data, metadata=metadata)

    def list_industry(self, ) -> ResponseData:
        """"""
        params = {"bkCode": "016", "_": str(int(time.time() * 1E3))}
        return self._get_data(params)

    def list_conception(self) -> ResponseData:
        """"""
        params = {"bkCode": "007", "_": str(int(time.time() * 1E3))}
        return self._get_data(params)

    def list_district(self) -> ResponseData:
        """"""
        params = {"bkCode": "020", "_": str(int(time.time() * 1E3))}
        return self._get_data(params)

    def get_code_by_name(self, name: str) -> pd.DataFrame:
        """"""
        df = pd.DataFrame(self.mapping_data)
        return df.loc[df.bkName.str.contains(name), ["bkCode", "bkName"]]

    def get_name_by_code(self, code: str) -> pd.DataFrame:
        """"""
        df = pd.DataFrame(self.mapping_data)
        return df.loc[df.bkCode == code, ["bkCode", "bkName"]]
