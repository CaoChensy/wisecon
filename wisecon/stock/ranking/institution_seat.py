from typing import Any, Dict, Optional, Callable, Literal
from wisecon.types import APIDataV1RequestData, BaseMapping


__all__ = [
    "InstitutionSeatMapping",
    "InstitutionSeat",
]


class InstitutionSeatMapping(BaseMapping):
    """字段映射 机构席位追踪"""
    columns: Dict = {
        "SECUCODE": "证券代码",
        "SECURITY_NAME_ABBR": "证券简称",
        "AMOUNT": "金额",
        "ONLIST_TIMES": "上榜次数",
        "BUY_AMT": "买入金额",
        "BUY_TIMES": "买入次数",
        "SELL_AMT": "卖出金额",
        "SELL_TIMES": "卖出次数",
        "NET_BUY_AMT": "净买入金额",
        "M1_CLOSE_ADJCHRATE": "1个月收盘调整幅度",
        "M3_CLOSE_ADJCHRATE": "3个月收盘调整幅度",
        "M6_CLOSE_ADJCHRATE": "6个月收盘调整幅度",
        "Y1_CLOSE_ADJCHRATE": "1年收盘调整幅度",
        "SECURITY_CODE": "证券代码",
        "CLOSE_PRICE": "收盘价格",
        "CHANGE_RATE": "变动率",
        "STATISTICSCYCLE": "统计周期",
        "BOARD_NAME": "板块名称",
        "BOARD_CODE": "板块代码",
        "SECURITY_TYPE_CODE": "证券类型代码"
    }


class InstitutionSeat(APIDataV1RequestData):
    """查询 机构席位追踪"""

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

            data = InstitutionSeat(statistics_cycle="1m").load()
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
        self.mapping = InstitutionSeatMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs
        self.request_set(description="机构席位追踪",)
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
            "sortColumns": "ONLIST_TIMES,SECURITY_CODE",
            "sortTypes": "-1,1",
            "reportName": "RPT_ORGANIZATION_SEATNEW",
        }
        return self.base_param(update=params)
