import json
from typing import Any, List, Dict, Callable, Literal, Optional
from wisecon.types import BaseMapping, BaseRequestData, Metadata
from wisecon.utils import headers, jquery_mock_callback, time2int, filter_str_by_mark


__all__ = [
    "FundTrendMapping",
    "FundTrend",
]


class FundTrendMapping(BaseMapping):
    """"""
    columns: Dict = {
        "date": "日期",
        "value": "累计收益",
        "hs_300": "沪深300",
        "sh_index": "上证指数",
    }


class FundTrend(BaseRequestData):
    """ Fund Trend """
    def __init__(
            self,
            fund_code: str,
            period: Literal["1m", "3m", "6m", "1y", "3y", "5y", "this_year", "all"] = "1y",
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        """"""
        self.fund_code = fund_code
        self.period = period
        self.mapping = FundTrendMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs

        self.request_set(
            response_type="text",
            description="基金趋势",
            other_headers={'Referer': 'https://fundf10.eastmoney.com/'},
        )

    def base_url(self) -> str:
        """"""
        base_url = "https://api.fund.eastmoney.com/f10/FundLJSYLZS/"
        return base_url

    def _param_dt(self) -> str:
        """"""
        dt_mapping = {
            "1m": "month", "3m": "threemonth", "6m": "sixmonth",
            "1y": "year", "3y": "threeyear", "5y": "fiveyear",
            "this_year": "thisyear", "all": "all"}
        return dt_mapping[self.period]

    def params(self) -> Dict:
        """
        :return:
        """
        params = {
            "callback": jquery_mock_callback(),
            "bzdm": self.fund_code,
            "dt": self._param_dt(),
            "_": time2int(),
        }
        return params

    def clean_content(
            self,
            content: Optional[str]
    ) -> List[Dict]:
        """"""
        content = filter_str_by_mark(content)
        response = json.loads(content)
        origin_data = response.pop("Data")
        columns = list(self.mapping.columns)
        data = [dict(zip(columns, item.split("_"))) for item in origin_data.split("|")]
        self.metadata.response = response
        return data
