from typing import Any, Dict, Optional, Literal, Callable
from wisecon.types import APIDataV1RequestData, BaseMapping


__all__ = [
    "DepartmentStatisticMapping",
    "DepartmentStatistic",
]


class DepartmentStatisticMapping(BaseMapping):
    """字段映射 营业部统计"""
    columns: Dict = {
        "OPERATEDEPT_CODE": "营业部代码",
        "OPERATEDEPT_NAME": "营业部名称",
        "STATISTICSCYCLE": "统计周期",
        "AMOUNT": "金额",
        "SALES_ONLIST_TIMES": "上榜成交次数",
        "ACT_BUY": "实际买入",
        "TOTAL_BUYER_SALESTIMES": "总买方成交次数",
        "ACT_SELL": "实际卖出",
        "TOTAL_SELLER_SALESTIMES": "总卖方成交次数",
        "OPERATEDEPT_CODE_OLD": "旧营业部代码",
        "ORG_NAME_ABBR": "组织名称简称"
    }


class DepartmentStatistic(APIDataV1RequestData):
    """查询 营业部统计"""

    def __init__(
            self,
            statistics_cycle: Literal["1m", "3m", "6m", "12m"] = "1m",
            size: Optional[int] = 20,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        """
        Notes:
            ```python
            from wisecon.stock.ranking import *

            data = DepartmentStatistic(statistics_cycle="1m").load()
            data.to_frame(chinese_column=True)
            ```

        Args:
            statistics_cycle: 统计周期, 可选值: 1m, 3m, 6m, 12m, 默认值: 1m
            size: 数据条数
            verbose: 是否打印日志
            logger: 日志记录器
            **kwargs: 其他参数
        """
        self.statistics_cycle = statistics_cycle
        self.size = size
        self.mapping = DepartmentStatisticMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs
        self.request_set(description="营业部统计",)
        self.conditions = []

    def params_statistics_cycle(self):
        """"""
        cycle_mapping = {"1m": "01", "3m": "02", "6m": "03", "12m": "04"}
        self.conditions.append(f'(STATISTICSCYCLE="{cycle_mapping.get(self.statistics_cycle, "01")}")')

    def params_filter(self) -> str:
        """"""
        self.params_statistics_cycle()
        return "".join(self.conditions)

    def params(self) -> Dict:
        """
        :return:
        """
        params = {
            "filter": self.params_filter(),
            "pageSize": self.size,
            "sortColumns": "AMOUNT,OPERATEDEPT_CODE",
            "sortTypes": "-1,1",
            "reportName": "RPT_OPERATEDEPT_LIST_STATISTICS",
        }
        return self.base_param(update=params)
