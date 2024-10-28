from typing import Any, Dict, Optional, Literal, Callable
from wisecon.types import APIMainHolder, BaseMapping


__all__ = [
    "MainHolderMapping",
    "MainHolder",
]


class MainHolderMapping(BaseMapping):
    """字段映射 机构持股一览表"""
    columns: Dict = {
        "SECURITY_INNER_CODE": "证券内部代码",
        "SECURITY_NAME_ABBR": "证券简称",
        "REPORT_DATE": "报告日期",
        "ORG_TYPE": "组织类型",
        "HOULD_NUM": "持有股数",
        "TOTAL_SHARES": "总股份数",
        "HOLD_VALUE": "持有市值",
        "FREESHARES_RATIO": "自由流通股比例",
        "HOLDCHA": "持仓变动",
        "HOLDCHA_NUM": "增仓股数",
        "HOLDCHA_RATIO": "增仓比例",
        "SECUCODE": "证券代码",
        "TOTALSHARES_RATIO": "总股份比例",
        "ORG_TYPE_NAME": "组织类型名称",
        "QCHANGE_RATE": "季度变动率",
        "FREE_MARKET_CAP": "自由流通市值",
        "FREE_SHARES": "自由流通股",
        "SECURITY_TYPE_CODE": "证券类型代码",
        "HOLDCHA_VALUE": "增仓市值",
        "SECURITY_CODE": "证券代码",
        "FREESHARES_RATIO_CHANGE": "自由流通股比例变动",
        "TYPE_NUM": "类型编号"
    }


class MainHolder(APIMainHolder):
    """查询 机构持股一览表"""

    def __init__(
            self,
            holder: Optional[Literal["基金", "QFII", "社保", "券商", "保险", "信托"]] = None,
            status: Optional[Literal["全部", "增持", "减持"]] = "全部",
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

            data = MainHolder(holder="基金", date="2024-09-30").load()
            data.to_frame(chinese_column=True)
            ```

        Args:
            holder: 机构类型
            status: 持股变动情况
            date: 查询日期
            size: 数据条数
            verbose: 是否打印日志
            logger: 日志记录器
            **kwargs: 其他参数
        """
        self.holder = holder
        self.status = status
        self.date = date
        self.size = size
        self.mapping = MainHolderMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs
        self.request_set(description="机构持股一览表",)
        self.validate_date_is_end_if_quarter(date=date)

    def params_holder_type(self) -> int:
        """"""
        holder_mapping = {"基金": 1, "QFII": 2, "社保": 3, "券商": 4, "保险": 5, "信托": 6}
        if self.holder in holder_mapping:
            return holder_mapping[self.holder]
        else:
            raise ValueError(f"holder_code must be in {holder_mapping.keys()}")

    def params_status(self) -> int:
        """"""
        status_mapping = {"全部": 0, "增持": 1, "减持": 2}
        if self.status in status_mapping:
            return status_mapping[self.status]
        else:
            raise ValueError(f"status must be in {status_mapping.keys()}")

    def params(self) -> Dict:
        """"""
        params = {
            "date": self.date,
            "type": self.params_holder_type(),
            "zjc": self.params_status(),
            "sortField": "HOULD_NUM",
            "pageSize": self.size,
        }
        return self.base_param(update=params)
