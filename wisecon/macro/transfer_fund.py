from typing import Any, Dict, Callable, Optional
from wisecon.types import BaseMapping
from .base import MacroRequestData


__all__ = [
    "TransferFundMapping",
    "TransferFund",
]


class TransferFundMapping(BaseMapping):
    """"""
    columns: Dict = {
        "START_DATE": "开始时间",
        "END_DATE": "截至时间",
        "END_SETTLE_BALANCE": "交易结算资金期末余额(亿)",
        "AVG_SETTLE_BALANCE": "交易结算资金日均余额(亿)",
        "SETTLE_FUNDS_ADD": "银证转账增加额(亿)",
        "SETTLE_FUNDS_REDUCE": "银证转账减少额(亿)",
        "SETTLE_FUNDS_NET": "银证转账变动净额(亿)",
        # "END_SETTLE_BALANCE_QOQ": "",
        # "AVG_SETTLE_BALANCE_QOQ": "",
        "INDEX_PRICE_SH": "上证指数收盘",
        "INDEX_PRICE_SZ": "深证指数收盘",
        # "INDEX_PRICE_CY": "",
        # "INDEX_PRICE_ZX": "",
        "INDEX_CHANGE_RATIO_SH": "上证指数涨跌幅",
        "INDEX_CHANGE_RATIO_SZ": "深证指数涨跌幅",
        # "INDEX_CHANGE_RATIO_CY": "",
        # "INDEX_CHANGE_RATIO_ZX": "",
    }


class TransferFund(MacroRequestData):
    """"""
    def __init__(
            self,
            size: Optional[int] = 20,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        self.size = size
        self.mapping = TransferFundMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs
        self.request_set(description="中国 交易结算资金(银证转账) 据投保基金公司2017年7月31日公告，该数据已停止更新。")

    def params(self) -> Dict:
        """
        :return:
        """
        columns = [
            "START_DATE", "END_DATE", "END_SETTLE_BALANCE", "AVG_SETTLE_BALANCE", "SETTLE_FUNDS_ADD",
            "SETTLE_FUNDS_REDUCE", "SETTLE_FUNDS_NET", "END_SETTLE_BALANCE_QOQ", "AVG_SETTLE_BALANCE_QOQ",
            "INDEX_PRICE_SH", "INDEX_PRICE_SZ", "INDEX_PRICE_CY", "INDEX_PRICE_ZX", "INDEX_CHANGE_RATIO_SH",
            "INDEX_CHANGE_RATIO_SZ", "INDEX_CHANGE_RATIO_CY", "INDEX_CHANGE_RATIO_ZX"
        ]
        params = {
            "columns": ",".join(columns),
            "pageSize": self.size,
            "sortColumns": "END_DATE",
            "sortTypes": "-1",
            "reportName": "RPT_BANKSECURITY_TRANSFER_FUND",
        }
        return self.base_param(update=params)
