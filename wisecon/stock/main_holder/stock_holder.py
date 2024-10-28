from typing import Any, Dict, Optional, Literal, Callable
from wisecon.types import APIMainHolderDetail, BaseMapping


__all__ = [
    "StockHolderMapping",
    "StockHolder",
]


class StockHolderMapping(BaseMapping):
    """字段映射 股票的机构持有者清单"""
    columns: Dict = {
        "SECUCODE": "证券代码",
        "SECURITY_CODE": "证券代码",
        "SECURITY_INNER_CODE": "证券内部代码",
        "SECURITY_NAME_ABBR": "证券简称",
        "REPORT_DATE": "报告日期",
        "HOLDER_CODE": "持有人代码",
        "HOLDER_NAME": "持有人名称",
        "PARENT_ORG_CODE": "母组织代码",
        "PARENT_ORGCODE_OLD": "旧母组织代码",
        "PARENT_ORG_NAME": "母组织名称",
        "ORG_TYPE_CODE": "组织类型代码",
        "ORG_TYPE": "组织类型",
        "TOTAL_SHARES": "总持股数",
        "HOLD_MARKET_CAP": "持有市值",
        "TOTAL_SHARES_RATIO": "总持股比例",
        "FREE_SHARES_RATIO": "自由流通股比例",
        "NETASSET_RATIO": "净资产比例",
        "ORG_NAME_ABBR": "组织名称简称",
        "BuyState": "购买状态"
    }


class StockHolder(APIMainHolderDetail):
    """查询 股票的机构持有者清单"""

    def __init__(
            self,
            security_code: Optional[str] = None,
            holder: Optional[Literal["基金", "QFII", "社保", "券商", "保险", "信托"]] = None,
            date: Optional[str] = None,
            size: Optional[int] = 50,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        """
        Notes:
            ```python
            from wisecon.stock.main_holder import *

            data = StockHolder(security_code="603350", holder="基金", date="2024-09-30").load()
            data.to_frame(chinese_column=True)
            ```

        Args:
            security_code: 股票代码
            holder: 机构类型
            date: 查询日期
            size: 数据条数
            verbose: 是否打印日志
            logger: 日志记录器
            **kwargs: 其他参数
        """
        self.security_code = security_code
        self.holder = holder
        self.date = date
        self.size = size
        self.mapping = StockHolderMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs
        self.request_set(description="股票的机构持有者清单",)
        self.validate_security_code(code=security_code)
        self.validate_date_is_end_if_quarter(date=date)

    def params_holder_type(self) -> int:
        """"""
        holder_mapping = {"基金": 1, "QFII": 2, "社保": 3, "券商": 4, "保险": 5, "信托": 6}
        if self.holder in holder_mapping:
            return holder_mapping[self.holder]
        else:
            raise ValueError(f"holder_code must be in {holder_mapping.keys()}")

    def params(self) -> Dict:
        """"""
        params = {
            "ReportDate": self.date,
            "SHType": self.params_holder_type(),
            "SCode": self.security_code,
            "sortField": "HOLDER_CODE",
            "pageSize": self.size,
        }
        return self.base_param(update=params)
