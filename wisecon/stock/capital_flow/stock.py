from typing import Any, Dict, Literal, Callable, Optional
from .base import CapitalFlowRequestData, CapitalFlowMapping


__all__ = [
    "StockFlowMapping",
    "StockFlow",
]


TypeMarketCode = Literal["全部股票", "沪深A股", "沪市A股", "科创板", "深市A股", "创业板", "沪市B股", "深市B股"]


class StockFlowMapping(CapitalFlowMapping):
    """字段映射 个股资金流向历史数据"""


class StockFlow(CapitalFlowRequestData):
    """查询 个股资金流向历史数据

    Notes:
        ```markdown
        指标定义
        　　- 超大单：大于等于50万股或者100万元的成交单;
        　　- 大单：大于等于10万股或者20万元且小于50万股和100万元的成交单;
        　　- 中单：大于等于2万股或者4万元且小于10万股和20万元的成交单;
        　　- 小单：小于2万股和4万元的成交单;
        　　- 流入：买入成交额;
        　　- 流出：卖出成交额;
        　　- 主力流入：超大单加大单买入成交额之和;
        　　- 主力流出：超大单加大单卖出成交额之和;
        　　- 净额：流入-流出;
        　　- 净比：(流入-流出)/总成交额;
        　　- 5日排名：5日主力净占比排名（指大盘连续交易的5日);
        　　- 5日涨跌：最近5日涨跌幅（指大盘连续交易的5日);
        　　- 10日排名：10日主力净占比排名（指大盘连续交易的10日);
        　　- 10日涨跌：最近10日涨跌幅（指大盘连续交易的10日);
        ```
    """
    def __init__(
            self,
            market: Optional[TypeMarketCode] = None,
            days: Optional[Literal[1, 3, 5, 10]] = 1,
            size: Optional[int] = 50,
            sort_by: Optional[str] = None,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        """
        Notes:
            ```python
            from wisecon.stock.capital_flow import *

            data = StockFlow(days=1).load()
            data.to_frame(chinese_column=True)
            ```

        Args:
            market: 市场名称 `["全部股票", "沪深A股", "沪市A股", "科创板", "深市A股", "创业板", "沪市B股", "深市B股"]`
            days: 统计天数 `1, 3, 5, 10`
            size: 返回数据量
            sort_by: 排序字段名称, 可通过`StockFlowMapping`查询
            verbose: 是否打印日志
            logger: 自定义日志函数
            **kwargs: 其他参数
        """
        self.market = market
        self.days = days
        self.size = size
        self.sort_by = sort_by
        self.mapping = StockFlowMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs
        self.request_set(description="个股资金流向历史数据", )

    def params_market(self) -> str:
        """"""
        market_mapping = {
            "全部股票": "m:0+t:6+f:!2,m:0+t:13+f:!2,m:0+t:80+f:!2,m:1+t:2+f:!2,m:1+t:23+f:!2,m:0+t:7+f:!2,m:1+t:3+f:!2",
            "沪深A股": "m:0+t:6+f:!2,m:0+t:13+f:!2,m:0+t:80+f:!2,m:1+t:2+f:!2,m:1+t:23+f:!2",
            "沪市A股": "m:1+t:2+f:!2,m:1+t:23+f:!2",
            "科创板": "m:1+t:23+f:!2",
            "深市A股": "m:0+t:6+f:!2,m:0+t:13+f:!2,m:0+t:80+f:!2",
            "创业板": "m:0+t:80+f:!2",
            "沪市B股": "m:1+t:3+f:!2",
            "深市B股": "m:0+t:7+f:!2"
        }
        if self.market in market_mapping:
            return market_mapping[self.market]
        else:
            return market_mapping["全部股票"]

    def params(self) -> Dict:
        """"""
        sort_by = self.params_sort_by()
        fields = self.params_fields()

        if sort_by not in fields:
            raise ValueError(f"Invalid sort_by value, please check the value in the `fields` attribute. {fields}")

        params = {
            "fid": sort_by,
            "po": 1,
            "pz": self.size,
            "pn": 1,
            "np": 1,
            "fltt": 2,
            "invt": 2,
            "fs": self.params_market(),
            "fields": fields,
        }
        return params
