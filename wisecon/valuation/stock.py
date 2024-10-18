from typing import Any, List, Dict, Callable, Optional
from wisecon.types import BaseMapping, ResponseData, BaseRequestData


__all__ = [
    "StockValuationMapping",
    "StockValuation",
]


class StockValuationMapping(BaseMapping):
    """"""
    columns: Dict = {
        "SECURITY_CODE": "股票编码",
        "SECUCODE": "股票编号",
        "SECURITY_NAME_ABBR": "股票简称",
        "ORG_CODE": "机构编码",
        "TRADE_MARKET": "市场编码",
        "BOARD_CODE": "行业编码",
        "BOARD_NAME": "行业",
        "ORIG_BOARD_CODE": "行业编号",
        "TOTAL_MARKET_CAP": "总市值",
        "NOTLIMITED_MARKETCAP_A": "无限制市值",
        "CLOSE_PRICE": "最新价",
        "CHANGE_RATE": "涨跌幅(%)",
        "TOTAL_SHARES": "总股份数",
        "FREE_SHARES_A": "自由流通股份",
        "PE_TTM": "PE(TTM)",
        "PE_LAR": "PE(静)",
        "PB_MRQ": "市净率",
        "PCF_OCF_LAR": "现金流比率",
        "PCF_OCF_TTM": "市现率",
        "PS_TTM": "市销率",
        "PEG_CAR": "PEG值",
        "TRADE_DATE": "交易日期"
    }


class StockValuation(BaseRequestData):
    """ ERF Market """
    def __init__(
            self,
            code: Optional[str] = None,
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
        self.code = code
        self.industry_code = industry_code
        self.date = date
        self.start_date = start_date
        self.end_date = end_date
        self.limit = limit
        self.mapping = StockValuationMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs

    def _base_url(self) -> str:
        """"""
        base_url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
        return base_url

    def _param_filter(self) -> str:
        """
        :return:
        """
        condition = []
        if self.date:
            condition.append(f"(TRADE_DATE='{self.date}')")
        elif self.start_date:
            condition.append(f"(TRADE_DATE>='{self.start_date}')")
        elif self.end_date:
            condition.append(f"(TRADE_DATE<='{self.end_date}')")
        else:
            raise ValueError("Either date or start_data must be provided")

        if self.industry_code:
            condition.append(f"(BOARD_CODE=\"{self.industry_code}\")")

        if self.code:
            condition.append(f"(SECURITY_CODE=\"{self.code}\")")
        return "".join(condition)

    def params(self) -> Dict:
        """
        :return:
        """
        params = {
            "pageSize": self.limit,
            "reportName": "RPT_VALUEANALYSIS_DET",
            "columns": "ALL",
            "quoteColumns": "",
            "pageNumber": 1,
            "sortColumns": "TRADE_DATE,SECURITY_CODE",
            "sortTypes": "-1,1",
            "source": "WEB",
            "client": "WEB",
            "filter": self._param_filter(),
            "_": 1728362858276,
        }
        return params

    def clean_data(self, data) -> List[Dict]:
        """"""
        columns = self.mapping.filter_columns(columns=self.mapping.columns)

        def _clean_data(item):
            """"""
            return {k: v for k, v in item.items() if k in columns}

        data = list(map(_clean_data, data))
        return data

    def load_data(self) -> ResponseData:
        """
        :return:
        """
        metadata = self.request_json().get("result", {})
        data = metadata.pop("data")
        data = self.clean_data(data=data)
        self.update_metadata(metadata)
        return ResponseData(data=data, metadata=metadata)

    def update_metadata(self, metadata: Dict):
        """"""
        columns = self.mapping.filter_columns(columns=self.mapping.columns)
        metadata.update({
            "description": "个股估值",
            "columns": columns,
        })
