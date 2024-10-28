from typing import Any, Dict, Callable, Optional
from wisecon.types import BaseMapping, APIDataV1RequestData


__all__ = [
    "StockValuationMapping",
    "StockValuation",
]


class StockValuationMapping(BaseMapping):
    """字段映射 个股估值"""
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
        "NOTsizeED_MARKETCAP_A": "无限制市值",
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


class StockValuation(APIDataV1RequestData):
    """查询 个股估值 """
    def __init__(
            self,
            security_code: Optional[str] = None,
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
            # 1. 查询全部股票的估值信息
            data = StockValuation(date="2024-09-30").load()
            data.to_frame(chinese_column=True)

            # 2. 查询某行业全部股票的估值信息
            data = StockValuation(date="2024-09-30", industry_code="016023").load()
            data.to_frame(chinese_column=True)

            # 3. 查询某只股票的估值信息
            data = StockValuation(start_data="2024-08-30", code="000059").load()
            data.to_frame(chinese_column=True)
            ```

        Args:
            security_code: 证券代码
            industry_code: 行业代码
            date: 交易日期
            start_date: 开始日期
            end_date: 结束日期
            size: 返回条数
            verbose: 是否打印日志
            logger: 自定义日志
            **kwargs: 其他参数
        """
        self.security_code = security_code
        self.industry_code = industry_code
        self.date = date
        self.start_date = start_date
        self.end_date = end_date
        self.size = size
        self.mapping = StockValuationMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs
        self.request_set(description="个股估值")
        self.conditions = []
        self.validate_date_format(date=[start_date, end_date, date])

    def params_filter(self) -> str:
        """
        :return:
        """
        self.filter_report_date(date_name="TRADE_DATE")
        if self.industry_code:
            self.validate_code(code=self.industry_code, length=6)
            self.conditions.append(f"(BOARD_CODE=\"{self.industry_code}\")")
        if self.security_code:
            self.validate_code(code=self.security_code, length=6)
            self.conditions.append(f"(SECURITY_CODE=\"{self.security_code}\")")
        return "".join(self.conditions)

    def params(self) -> Dict:
        """
        :return:
        """
        params = {
            "pageSize": self.size,
            "reportName": "RPT_VALUEANALYSIS_DET",
            "sortColumns": "TRADE_DATE,SECURITY_CODE",
            "sortTypes": "-1,1",
            "filter": self.params_filter(),
        }
        return self.base_param(update=params)
