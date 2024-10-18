from typing import Any, Dict, Callable, Optional
from wisecon.types import BaseMapping
from .base import MacroRequestData


__all__ = [
    "DepositRateMapping",
    "DepositRate",
]


class DepositRateMapping(BaseMapping):
    """"""
    columns: Dict = {
        "REPORT_DATE": "公布时间",
        "PUBLISH_DATE": "生效时间",
        "DEPOSIT_RATE_BB": "存款基准利率(调整前)",
        "DEPOSIT_RATE_BA": "存款基准利率(调整后)",
        "DEPOSIT_RATE_B": "存款基准利率(调整幅度)",
        "LOAN_RATE_SB": "贷款基准利率(调整前)",
        "LOAN_RATE_SA": "贷款基准利率(调整后)",
        "LOAN_RATE_S": "贷款基准利率(调整幅度)",
        "NEXT_SH_RATE": "消息公布次日指数涨跌(SH)",
        "NEXT_SZ_RATE": "消息公布次日指数涨跌(SZ)",
    }


class DepositRate(MacroRequestData):
    """"""
    def __init__(
            self,
            size: Optional[int] = 20,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        self.size = size
        self.mapping = DepositRateMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs
        self.request_set(
            response_type="json",
            description="中国 利率调整",
        )

    def params(self) -> Dict:
        """
        :return:
        """
        columns = [
            "REPORT_DATE", "PUBLISH_DATE", "DEPOSIT_RATE_BB", "DEPOSIT_RATE_BA", "DEPOSIT_RATE_B", "LOAN_RATE_SB",
            "LOAN_RATE_SA", "LOAN_RATE_S", "NEXT_SH_RATE", "NEXT_SZ_RATE",
        ]
        params = {
            "columns": ",".join(columns),
            "pageSize": self.size,
            "sortColumns": "REPORT_DATE",
            "sortTypes": "-1",
            "reportName": "RPT_ECONOMY_DEPOSIT_RATE",
        }
        return self.base_param(update=params)
