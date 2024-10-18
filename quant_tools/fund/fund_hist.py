import json
import requests
from functools import partial
from typing import Any, List, Dict, Callable, Optional
from quant_tools.types import BaseMapping, BaseRequestData, Metadata, ResponseData
from quant_tools.utils import headers, LoggerMixin, jquery_mock_callback, time2int, filter_dict_by_key


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


class FundHist(BaseRequestData):
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
        self.request_set(
            response_type="text",
            description="基金历史净值",
            other_headers={'Referer': 'https://fundf10.eastmoney.com/'},
        )

    def base_url(self) -> str:
        """"""
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

    def clean_content(
            self,
            content: Optional[str] = None,
    ) -> List[Dict]:
        """"""
        content = content[content.find("(") + 1: content.rfind(")")]
        response = json.loads(content).pop("Data")
        data = response.pop("LSJZList")

        _filter_dict = partial(filter_dict_by_key, keys=list(self.mapping.columns.keys()))
        data = list(map(_filter_dict, data))
        self.metadata.response = response
        return data
