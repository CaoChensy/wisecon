import requests
import pandas as pd
from requests import Response
from tqdm import tqdm
from typing import List, Dict, Optional

from wisecon.types import ResponseData
from wisecon.types.request_data import BaseRequestData


__all__ = [
    "APICurrentCarRequestData",
    "APICarHistoryRequestData",
]


class APICurrentCarRequestData(BaseRequestData):
    """"""
    def base_url(self) -> str:
        return "https://xl.16888.com/xl.php"

    def base_param(self, update: Dict) -> Dict:
        """"""
        params = {
            "mod": "api",
            "extra": "factoryRanking",
        }
        params.update(update)
        return params

    def clean_json(
            self,
            json_data: Optional[Dict],
    ) -> List[Dict]:
        """"""
        response = json_data.get("data", {})
        data = response.pop("list")
        self.metadata.response = response
        return data


class APICarHistoryRequestData(BaseRequestData):
    """"""
    data_mark: Optional[str]
    page: Optional[int]
    data_page_name: Optional[str]
    multi_pages: Optional[bool]

    def base_url(self, **kwargs) -> str:
        return f"https://xl.16888.com/{self.data_page_name}.html"

    def request(self, **kwargs) -> Response:
        """"""
        base_url = self.base_url(**kwargs)
        self._logger(msg=f"URL: {base_url}\n", color="green")
        response = requests.get(base_url, headers=self.headers)
        return response

    def request_data(self, df_list: List) -> bool:
        """"""
        self.data_page_name = f"{self.data_mark}-{self.page}"
        content = self.request().content
        df = pd.read_html(content)[0]
        if len(df) > 1:
            df_list.append(df)
            self.page += 1
            mark = True
        else:
            mark = False
        return mark

    def request_html(self) -> List[Dict]:
        """"""
        self.data_page_name = self.data_mark
        content = self.request().content
        df = pd.read_html(content)[0]
        return df.to_dict(orient="records")

    def request_mutil_html(self, ) -> List[Dict]:
        self.page = 1
        mark = True
        df_list = []

        if self.verbose:
            with tqdm() as pbar:
                while mark:
                    mark = self.request_data(df_list)
                    pbar.update(1)
        else:
            while mark:
                mark = self.request_data(df_list)
        df = pd.concat(df_list, ignore_index=True)
        return df.to_dict(orient="records")

    def load(self) -> ResponseData:
        """"""
        if self.response_type == "html":
            if self.multi_pages:
                data = self.request_mutil_html()
            else:
                data = self.request_html()
        else:
            raise NotImplementedError("Not implemented yet")
        return self.data(data=data, metadata=self.metadata)
