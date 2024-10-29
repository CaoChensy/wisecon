from typing import Any, Dict, Optional, Literal, Callable
from wisecon.types import APIDataV1RequestData, BaseMapping


__all__ = [
    "StockRankStatisticMapping",
    "StockRankStatistic",
]


class StockRankStatisticMapping(BaseMapping):
    """字段映射 个股上榜统计"""
    columns: Dict = {
        "SECUCODE": "证券代码",
        "SECURITY_CODE": "证券代码",
        "LATEST_TDATE": "最新交易日期",
        "SECURITY_NAME_ABBR": "证券简称",
        "IPCT1M": "1个月涨幅",
        "IPCT3M": "3个月涨幅",
        "IPCT6M": "6个月涨幅",
        "IPCT1Y": "1年涨幅",
        "CHANGE_RATE": "变动率",
        "CLOSE_PRICE": "收盘价格",
        "PERIOD": "统计周期",
        "BILLBOARD_DEAL_AMT": "排行榜成交金额",
        "BILLBOARD_NET_BUY": "排行榜净买入",
        "ORG_TIMES": "机构交易次数",
        "ORG_DEAL_AMT": "机构成交金额",
        "ORG_NET_BUY": "机构净买入",
        "BILLBOARD_TIMES": "排行榜交易次数",
        "BILLBOARD_BUY_AMT": "排行榜买入金额",
        "BILLBOARD_SELL_AMT": "排行榜卖出金额",
        "ORG_BUY_AMT": "机构买入金额",
        "ORG_SELL_AMT": "机构卖出金额",
        "ORG_BUY_TIMES": "机构买入次数",
        "ORG_SELL_TIMES": "机构卖出次数",
        "STATISTICS_CYCLE": "统计周期",
        "SECURITY_TYPE_CODE": "证券类型代码"
    }


class StockRankStatistic(APIDataV1RequestData):
    """查询 个股上榜统计"""

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

            data = StockRankStatistic(statistics_cycle="1m").load()
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
        self.mapping = StockRankStatisticMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs
        self.request_set(description="个股上榜统计",)
        self.conditions = []

    def params_statistics_cycle(self):
        """"""
        cycle_mapping = {"1m": "01", "3m": "02", "6m": "03", "12m": "04"}
        self.conditions.append(f'(STATISTICS_CYCLE="{cycle_mapping.get(self.statistics_cycle, "01")}")')

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
            "sortColumns": "BILLBOARD_TIMES,LATEST_TDATE,SECURITY_CODE",
            "sortTypes": "-1,-1,1",
            "reportName": "RPT_BILLBOARD_TRADEALLNEW",
        }
        return self.base_param(update=params)
