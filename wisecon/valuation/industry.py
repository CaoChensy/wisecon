from typing import Any, List, Dict, Callable, Optional
from wisecon.types import BaseMapping, BaseRequestData
from wisecon.utils import time2int


__all__ = [
    "IndustryValuationMapping",
    "IndustryValuation",
]


class IndustryValuationMapping(BaseMapping):
    """"""
    columns: Dict = {
        "BOARD_NAME": "行业",
        "BOARD_CODE": "行业代码",
        "ORIGINALCODE": "行业编码",
        "TRADE_DATE": "交易日期",
        "PE_TTM": "PE(TTM)",
        "PE_LAR": "PE(静)",
        "PB_MRQ": "市净率",
        "PCF_OCF_TTM": "市现率",
        "PS_TTM": "市销率",
        "PEG_CAR": "PEG值",
        "TOTAL_MARKET_CAP": "总市值",
        "MARKET_CAP_VAG": "平均市值",
        "NOTLIMITED_MARKETCAP_A": "非限制市值",
        "NOMARKETCAP_A_VAG": "无市场价值的可变资产",
        "TOTAL_SHARES": "总股份",
        "TOTAL_SHARES_VAG": "可变股份总数",
        "FREE_SHARES_VAG": "平均市值",
        "NUM": "个股数量",
        "LOSS_COUNT": "亏损家数"
    }


class IndustryValuation(BaseRequestData):
    """ ERF Market """
    def __init__(
            self,
            industry_code: Optional[str] = None,
            date: Optional[str] = None,
            start_date: Optional[str] = None,
            end_date: Optional[str] = None,
            limit: Optional[int] = 50,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        """"""
        self.industry_code = industry_code
        self.date = date
        self.start_date = start_date
        self.end_date = end_date
        self.limit = limit
        self.mapping = IndustryValuationMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs
        self.request_set(description="中国 行业市场估值")

    def base_url(self) -> str:
        """"""
        base_url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
        return base_url

    def _param_filter(self) -> str:
        """"""
        condition = []
        if self.date:
            condition.append(f"(TRADE_DATE='{self.date}')")
        if self.start_date:
            condition.append(f"(TRADE_DATE>='{self.start_date}')")
        if self.end_date:
            condition.append(f"(TRADE_DATE<='{self.end_date}')")

        if self.industry_code:
            condition.append(f"(BOARD_CODE=\"{self.industry_code}\")")
        return "".join(condition)

    def params(self) -> Dict:
        """
        :return:
        """
        params = {
            "pageSize": self.limit,
            "reportName": "RPT_VALUEINDUSTRY_DET",
            "columns": "ALL",
            "quoteColumns": "",
            "pageNumber": 1,
            "sortColumns": "TRADE_DATE,PE_TTM",
            "sortTypes": "-1,1",
            "source": "WEB",
            "client": "WEB",
            "filter": self._param_filter(),
            "_": time2int(),
        }
        return params

    def clean_json(
            self,
            json_data: Optional[Dict],
    ) -> List[Dict]:
        """"""
        response = json_data.get("result")
        data = response.pop("data")
        self.metadata.response = response

        columns = self.mapping.filter_columns(columns=self.mapping.columns)

        def _clean_data(item):
            """"""
            return {k: v for k, v in item.items() if k in columns}

        data = list(map(_clean_data, data))
        return data
