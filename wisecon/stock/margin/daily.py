from typing import Any, Dict, Callable, Optional
from wisecon.types import BaseMapping, APIDataRequestData


__all__ = [
    "MarginTradingDailyMapping",
    "MarginTradingDaily",
]


class MarginTradingDailyMapping(BaseMapping):
    """字段映射 融资融券交易总量"""
    columns: Dict = {
        "TRADE_DATE": "交易日期",
        "MARKET": "市场",
        "BOARD_CODE": "板块代码",
        "FIN_BALANCE": "融资余额",
        "LOAN_BALANCE": "借入余额",
        "MARGIN_BALANCE": "保证金余额",
        "FIN_BUY_AMT": "融资买入金额"
    }


class MarginTradingDaily(APIDataRequestData):
    """查询 融资融券交易总量"""
    def __init__(
            self,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        """
        Notes:
            ```python
            from wisecon.stock.margin import *

            # 查询 融资融券交易总量-市场合计
            data = MarginTradingDaily().load()
            data.to_frame(chinese_column=True)
            ```

        Args:
            verbose: 是否打印日志
            logger: 自定义日志打印函数
            **kwargs: 其他参数
        """
        self.mapping = MarginTradingDailyMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs
        self.request_set(description="融资融券交易总量")
        self.conditions = []

    def params(self) -> Dict:
        """"""
        columns = [
            "TRADE_DATE", "MARKET", "BOARD_CODE", "FIN_BALANCE",
            "LOAN_BALANCE", "MARGIN_BALANCE", "FIN_BUY_AMT",
        ]
        params = {
            "type": "RPT_MARGIN_MARGINPROFILE",
            "sty": ",".join(columns),
            "p": "1",
            "ps": "5",
        }
        return self.base_param(update=params)
