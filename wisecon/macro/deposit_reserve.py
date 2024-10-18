from typing import Any, Dict, Callable, Optional
from wisecon.types import BaseMapping
from .base import MacroRequestData


__all__ = [
    "DepositReserveMapping",
    "DepositReserve",
]


class DepositReserveMapping(BaseMapping):
    """"""
    columns: Dict = {
        "REPORT_DATE": "报告时间",
        "PUBLISH_DATE": "公布时间",
        "TRADE_DATE": "生效时间",
        "INTEREST_RATE_BB": "大型金融机构（调整前）",
        "INTEREST_RATE_BA": "大型金融机构（调整后）",
        "CHANGE_RATE_B": "大型金融机构（调整幅度）",
        "INTEREST_RATE_SB": "中小金融机构（调整前）",
        "INTEREST_RATE_SA": "中小金融机构（调整后）",
        "CHANGE_RATE_S": "中小金融机构（调整幅度）",
        "NEXT_SH_RATE": "消息公布次日指数涨跌（上证-SH）",
        "NEXT_SZ_RATE": "消息公布次日指数涨跌（深证-SZ）",
        "REMARK": "消息",
    }


class DepositReserve(MacroRequestData):
    """"""
    def __init__(
            self,
            size: Optional[int] = 20,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        self.size = size
        self.mapping = DepositReserveMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs
        self.request_set(description="中国 存款准备金率")

    def params(self) -> Dict:
        """
        :return:
        """
        columns = [
            "REPORT_DATE", "PUBLISH_DATE", "TRADE_DATE", "INTEREST_RATE_BB", "INTEREST_RATE_BA",
            "CHANGE_RATE_B", "INTEREST_RATE_SB", "INTEREST_RATE_SA", "CHANGE_RATE_S", "NEXT_SH_RATE",
            "NEXT_SZ_RATE", "REMARK",
        ]
        params = {
            "columns": ",".join(columns),
            "pageSize": self.size,
            "sortColumns": "PUBLISH_DATE,TRADE_DATE",
            "sortTypes": "-1,-1",
            "reportName": "RPT_ECONOMY_DEPOSIT_RESERVE",
        }
        return self.base_param(update=params)
