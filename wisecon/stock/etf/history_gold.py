from typing import Any, Dict, Callable, Optional, Literal
from wisecon.types import BaseMapping, APIDataV1RequestData


__all__ = [
    "ETFGoldHistoryMapping",
    "ETFGoldHistory",
]


class ETFGoldHistoryMapping(BaseMapping):
    """字段映射 白银/黄金ETF历史行情"""
    columns: Dict = {
        "REPORT_DATE": "报告日期",
        "INDICATOR_NAME": "指标名称",
        "INDICATOR_ID1": "指标ID1",
        "STORAGE_TON": "库存（吨）",
        "STORAGE_OUNCE": "库存（盎司）",
        "INDICATOR_ID2": "指标ID2",
        "NETPOSITION_TON": "净头寸（吨）",
        "NETPOSITION_OUNCE": "净头寸（盎司）",
        "NETPOSITION_DOLLAR": "净头寸（美元）",
        "INDICATOR_ID3": "指标ID3",
        "OPENPOSI_STOCK": "开盘持仓",
        "OPENPOSTOCK_WECHANGE": "开盘持仓变动",
        "OPENPOSI_STOCK_SUM": "开盘持仓总和"
    }


class ETFGoldHistory(APIDataV1RequestData):
    """查询 白银/黄金ETF历史行情"""
    def __init__(
            self,
            market: Literal["ETF白银", "ETF黄金"] = "ETF黄金",
            start_date: Optional[str] = None,
            end_date: Optional[str] = None,
            date: Optional[str] = None,
            size: Optional[int] = 100,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        """
        Notes:
            ```python
            from wisecon.stock.etf import *

            # 1. 查询 ETF白银历史行情
            data = ETFGoldHistory(market="ETF白银").load()
            data.to_frame(chinese_column=True)

            # 2. 查询 ETF黄金某时点
            data = ETFGoldHistory(market="ETF黄金", date="2024-10-25").load()
            data.to_frame(chinese_column=True)

            # 3. 查询 ETF黄金历史行情，并指定查询开始日期
            data = ETFGoldHistory(market="ETF黄金", start_date="2024-10-25").load()
            data.to_frame(chinese_column=True)
            ```

        Args:
            market: 市场类型
            start_date: 开始日期
            end_date: 结束日期
            date: 查询日期
            size: 返回数据量
            verbose: 是否打印日志
            logger: 自定义日志打印函数
            **kwargs: 其他参数
        """
        self.market = market
        self.size = size
        self.start_date = start_date
        self.end_date = end_date
        self.date = date
        self.mapping = ETFGoldHistoryMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs
        self.request_set(description="白银/黄金ETF历史行情")
        self.conditions = []
        self.validate_date_format(date=[start_date, end_date, date])

    def params_filter(self) -> str:
        """"""
        market_mapping = {
            "ETF白银": '(INDICATOR_ID2="EMI00223868")(@NETPOSITION_TON<>"NULL")',
            "ETF黄金": '(INDICATOR_ID2="EMI00223865")(@NETPOSITION_TON<>"NULL")',
        }
        self.conditions.append(market_mapping[self.market])
        self.filter_report_date(date_name="REPORT_DATE")
        return "".join(self.conditions)

    def params(self) -> Dict:
        """"""
        params = {
            "sortColumns": "REPORT_DATE",
            "sortTypes": "-1",
            "pageSize": self.size,
            "reportName": "RPT_FUTUOPT_GOLDSIL",
            "filter": self.params_filter(),
        }
        return self.base_param(update=params)
