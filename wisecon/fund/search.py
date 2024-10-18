import json
import requests
from functools import partial
from typing import Any, List, Dict, Callable, Optional
from wisecon.types import BaseMapping, ResponseData
from wisecon.utils import headers, LoggerMixin, jquery_mock_callback, time2int, filter_dict_by_key


__all__ = [
    "FundHistMapping",
    "FundHist",
]


class FundHistMapping(BaseMapping):
    """"""
    columns: Dict = {
        "FSRQ": "净值日期",
        "DWJZ": "单位净值",
        "LJJZ": "累计净值",
        "JZZZL": "日增长率",
        "SGZT": "申购状态",
        "SHZT": "赎回状态",
    }


class FundHist(LoggerMixin):
    """ Fund History """
    def __init__(
            self,
            fund_code: str,
            start_date: Optional[str] = "",
            end_date: Optional[str] = "",
            limit: Optional[int] = 20,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        """"""
        self.fund_code = fund_code
        self.start_date = start_date
        self.end_date = end_date
        self.limit = limit
        self.mapping = FundHistMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs

    def _base_url(self) -> str:
        """
        https://fund.eastmoney.com/data/FundGuideapi.aspx?
        dt=4
        sd=
        ed=
        tp=BK000174
        se>5
        sc=2n
        st=desc
        pi=1
        pn=27
        zf=diy
        sh=list
        rnd=0.13975355548916668


        :return:
        """
        base_url = "https://api.fund.eastmoney.com/f10/lsjz"
        return base_url

    def params(self) -> Dict:
        """
        :return:
        """
        params = {
            "callback": jquery_mock_callback(),
            "fundCode": self.fund_code,
            "pageIndex": "1",
            "pageSize": self.limit,
            "startDate": self.start_date,
            "endDate": self.end_date,
            "_": time2int(),
        }
        return params

    def request_json(self) -> Dict:
        """
        :return:
        """
        headers.update({'Referer': 'https://fundf10.eastmoney.com/'})
        response = requests.get(self._base_url(), params=self.to_params(), headers=headers)
        content = response.text
        content = content[content.find("(") + 1: content.rfind(")")]
        data = json.loads(content)
        return data

    def clean_data(self, data: List[Dict]) -> List[Dict]:
        """"""
        _filter_dict = partial(filter_dict_by_key, keys=list(self.mapping.columns.keys()))
        data = list(map(_filter_dict, data))
        return data

    def load_data(self) -> ResponseData:
        """
        :return:
        """
        metadata = self.request_json()
        data = metadata.pop("Data")
        data = self.clean_data(data.get("LSJZList"))
        self.update_metadata(metadata)
        return ResponseData(data=data, metadata=metadata)

    def update_metadata(self, metadata: Dict):
        """"""
        columns = self.mapping.filter_columns(columns=self.mapping.columns)
        metadata.update({
            "description": "基金历史净值",
            "columns": columns,
        })
