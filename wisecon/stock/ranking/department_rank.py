from typing import Any, Dict, Optional, Literal, Callable
from wisecon.types import APIDataV1RequestData, BaseMapping


__all__ = [
    "DepartmentRankMapping",
    "DepartmentRank",
]


class DepartmentRankMapping(BaseMapping):
    """字段映射 营业部排行"""
    columns: Dict = {
        "OPERATEDEPT_CODE": "营业部代码",
        "OPERATEDEPT_NAME": "营业部名称",
        "STATISTICSCYCLE": "统计周期",
        "AVERAGE_INCREASE_1DAY": "1日平均涨幅",
        "RISE_PROBABILITY_1DAY": "1日上涨概率",
        "TOTAL_BUYER_SALESTIMES_1DAY": "1日总买方成交次数",
        "AVERAGE_INCREASE_2DAY": "2日平均涨幅",
        "RISE_PROBABILITY_2DAY": "2日上涨概率",
        "TOTAL_BUYER_SALESTIMES_2DAY": "2日总买方成交次数",
        "AVERAGE_INCREASE_3DAY": "3日平均涨幅",
        "RISE_PROBABILITY_3DAY": "3日上涨概率",
        "TOTAL_BUYER_SALESTIMES_3DAY": "3日总买方成交次数",
        "AVERAGE_INCREASE_5DAY": "5日平均涨幅",
        "RISE_PROBABILITY_5DAY": "5日上涨概率",
        "TOTAL_BUYER_SALESTIMES_5DAY": "5日总买方成交次数",
        "AVERAGE_INCREASE_10DAY": "10日平均涨幅",
        "RISE_PROBABILITY_10DAY": "10日上涨概率",
        "TOTAL_BUYER_SALESTIMES_10DAY": "10日总买方成交次数",
        "OPERATEDEPT_CODE_OLD": "旧营业部代码"
    }


class DepartmentRank(APIDataV1RequestData):
    """查询 营业部排行"""

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

            data = DepartmentRank(statistics_cycle="1m").load()
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
        self.mapping = DepartmentRankMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs
        self.request_set(description="营业部排行",)
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
        """"""
        params = {
            "filter": self.params_filter(),
            "pageSize": self.size,
            "sortColumns": "TOTAL_BUYER_SALESTIMES_1DAY,OPERATEDEPT_CODE",
            "sortTypes": "-1,1",
            "reportName": "RPT_RATEDEPT_RETURNT_RANKING",
        }
        return self.base_param(update=params)
