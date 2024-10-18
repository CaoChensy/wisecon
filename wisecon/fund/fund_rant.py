import json
import requests
from typing import Any, List, Dict, Callable, Literal, Optional
from wisecon.types import BaseMapping, ResponseData, BaseRequestData
from wisecon.utils import (
    headers, LoggerMixin, jquery_mock_callback, time2int,
    filter_str_by_mark
)


__all__ = [
    "FundRantMapping",
    "FundRant",
]


class FundRantMapping(BaseMapping):
    """"""
    columns: Dict = {
        "date": "日期",
        "rant": "排名",
    }


class FundRant(BaseRequestData):
    """ Fund History """
    def __init__(
            self,
            fund_code: str,
            period: Literal["1m", "3m", "6m", "1y", "3y", "5y", "this_year", "all"] = "1y",
            observation: Literal["3m", "6m", "1y"] = "3m",
            percent: Optional[bool] = False,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        """"""
        self.fund_code = fund_code
        self.period = period
        self.percent = percent
        self.observation = observation
        self.mapping = FundRantMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs
        self.dt_mapping = {
            "1m": "month", "3m": "threemonth", "6m": "sixmonth",
            "1y": "year", "3y": "threeyear", "5y": "fiveyear",
            "this_year": "thisyear", "all": "all"}
        self.request_set(
            response_type="text",
            description="基金排名",
            other_headers={'Referer': 'https://fundf10.eastmoney.com/'},
        )

    def base_url(self) -> str:
        """
        :return:
        """
        mark_type = "FundBFBPM" if self.percent else "FundTLPM"
        base_url = f"https://api.fund.eastmoney.com/f10/{mark_type}/"
        return base_url

    def params(self) -> Dict:
        """
        :return:
        """
        params = {
            "callback": jquery_mock_callback(),
            "bzdm": self.fund_code,
            "dt": self.dt_mapping.get(self.period, "year"),
            "rt": self.dt_mapping.get(self.observation, "threemonth"),
            "_": time2int(),
        }
        return params

    def clean_content(
            self,
            content: Optional[str],
    ) -> List[Dict]:
        """"""
        content = filter_str_by_mark(content)
        response = json.loads(content)

        columns = list(self.mapping.columns)
        data = response.pop("Data")
        data = [dict(zip(columns, item.split("_"))) for item in data.split("|")]

        self.metadata.response = response
        return data
