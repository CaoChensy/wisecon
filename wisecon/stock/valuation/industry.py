from typing import Any, Dict, Callable, Optional
from wisecon.types import BaseMapping, APIDataV1RequestData


__all__ = [
    "IndustryValuationMapping",
    "IndustryValuation",
]


class IndustryValuationMapping(BaseMapping):
    """字段映射 上市公司行业估值"""
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


class IndustryValuation(APIDataV1RequestData):
    """查询 上市公司行业估值"""
    def __init__(
            self,
            industry_code: Optional[str] = None,
            date: Optional[str] = None,
            start_date: Optional[str] = None,
            end_date: Optional[str] = None,
            size: Optional[int] = 50,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        """
        Notes:
            ```python
            # 1. 查询某日期全部行业估值
            data = IndustryValuation(date="2024-10-10").load()
            data.to_frame(chinese_column=True)

            # 2. 查询某周期某行业估值
            data = IndustryValuation(
                start_date="2024-10-01", end_date="2024-10-20",
                limit=50, industry_code="016017"
            ).load()
            data.to_frame(chinese_column=True)
            ```

        Args:
            industry_code: 行业代码
            date: 查询日期
            start_date: 开始日期
            end_date: 结束日期
            size: 返回条数
            verbose: 是否打印日志
            logger: 自定义日志
            **kwargs: 其他参数
        """
        self.industry_code = industry_code
        self.date = date
        self.start_date = start_date
        self.end_date = end_date
        self.size = size
        self.mapping = IndustryValuationMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs
        self.conditions = []
        self.validate_date_format(date=[start_date, end_date, date], )
        self.request_set(description="上市公司行业估值")

    def params_industry_code(self):
        """"""
        if self.industry_code:
            self.validate_code(self.industry_code, length=6)
            self.conditions.append(f"(BOARD_CODE=\"{self.industry_code}\")")

    def params_filter(self) -> str:
        """"""
        self.filter_report_date(date_name="TRADE_DATE")
        self.params_industry_code()
        return "".join(self.conditions)

    def params(self) -> Dict:
        """
        :return:
        """
        params = {
            "pageSize": self.size,
            "reportName": "RPT_VALUEINDUSTRY_DET",
            "pageNumber": 1,
            "sortColumns": "TRADE_DATE,PE_TTM",
            "sortTypes": "-1,1",
            "filter": self.params_filter(),
        }
        return self.base_param(update=params)
