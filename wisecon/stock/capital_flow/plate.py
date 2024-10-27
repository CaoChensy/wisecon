from typing import Any, Dict, Literal, Callable, Optional
from .base import TypeMarket, CapitalFlowRequestData, CapitalFlowMapping


__all__ = [
    "PlateFlowMapping",
    "PlateFlow",
]


class PlateFlowMapping(CapitalFlowMapping):
    """字段映射 市场、板块（行业、概念、地区）资金流向数据"""


class PlateFlow(CapitalFlowRequestData):
    """查询 市场、板块（行业、概念、地区）资金流向数据

    1. 查询市场总体资金流量；返回全部股票当前`1/3/5/10`天的资金动向
    2. 查询全部 `行业、地区、概念` 板块资金流量；返回全部板块下股票当前`1/3/5/10`天的资金动向
    3. 查询指定板块资金流量；返回具体板块下股票当前`1/3/5/10`天的资金动向
    4. 查询不同行业、地区、概念板块下的主力流入流出排名

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
            market: Optional[TypeMarket] = None,
            plate_type: Optional[Literal["行业", "概念", "地区"]] = None,
            plate_code: Optional[str] = None,
            size: Optional[int] = 50,
            sort_by: Optional[str] = None,
            ascending: Optional[bool] = False,
            days: Optional[Literal[1, 3, 5, 10]] = None,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        """
        Notes:
            ```python
            from wisecon.stock.capital_flow import *

            # 1. 查询市场总体资金流量
            data = PlateFlow(market="沪深A股", days=1).load()
            data.to_frame(chinese_column=True)

            # 2. 查询全部 `行业、地区、概念` 板块资金流量
            data = PlateFlow(plate_type="行业", days=1).load()
            data.to_frame(chinese_column=True)

            # 3. 查询指定板块资金流量
            # 3.1 行业板块
            data = PlateFlow(plate_code="BK1027", days=1).load()
            data.to_frame(chinese_column=True)

            # 3.1 地区板块
            data = PlateFlow(plate_code="BK0158", days=1).load()
            data.to_frame(chinese_column=True)

            # 3.1 概念板块
            data = PlateFlow(plate_code="BK1044", days=1).load()
            data.to_frame(chinese_column=True)

            # 4. 主力排名
            data = PlateFlow(market="全部股票", sort_by="f184").load()
            data.to_frame(chinese_column=True)

            # 4.1 主力流入排名
            PlateFlow(plate_type="行业", days=1, sort_by="f62")
            PlateFlow(plate_type="行业", days=3, sort_by="f267")
            PlateFlow(plate_type="行业", days=5, sort_by="f164")
            PlateFlow(plate_type="行业", days=10, sort_by="f174")

            # 4.2 主力流出排名
            PlateFlow(plate_type="行业", days=1, sort_by="f62", ascending=True)
            PlateFlow(plate_type="行业", days=3, sort_by="f267", ascending=True)
            PlateFlow(plate_type="行业", days=5, sort_by="f164", ascending=True)
            PlateFlow(plate_type="行业", days=10, sort_by="f174", ascending=True)
            ```

        Args:
            market: 市场名称 `["全部股票", "沪深A股", "沪市A股", "科创板", "深市A股", "创业板", "沪市B股", "深市B股"]`
            plate_type: 板块类型, `["行业", "概念", "地区"]`
            plate_code: 板块代码, 支持行业、概念、地区等代码
            days: 统计天数 `1, 3, 5, 10`
            size: 返回数据量
            sort_by: 排序字段名称, 可通过 `PlateFlowMapping` 查询
            verbose: 是否打印日志
            logger: 自定义日志函数
            **kwargs: 其他参数
        """
        self.market = market
        self.plate_type = plate_type
        self.plate_code = plate_code
        self.size = size
        self.sort_by = sort_by
        self.ascending = ascending
        self.days = days
        self.mapping = PlateFlowMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs
        self.request_set(description="市场、板块（行业、概念、地区）资金流向数据", )

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

    def params_plate_type(self) -> str:
        """"""
        plate_mapping = {
            "行业": "m:90+t:2",
            "概念": "m:90+t:3",
            "地区": "m:90+t:1",
        }
        if self.plate_type in plate_mapping:
            return plate_mapping[self.plate_type]
        else:
            return plate_mapping["行业"]

    def params_plate_code(self) -> str:
        """"""
        return f"b:{self.plate_code}"

    def params_ascending(self) -> int:
        if self.ascending:
            return 0
        else:
            return 1

    def params_fs(self) -> str:
        """"""
        if self.market:
            return self.params_market()
        elif self.plate_type:
            return self.params_plate_type()
        elif self.plate_code:
            return self.params_plate_code()
        else:
            raise ValueError(
                "Invalid parameters, please check the value in the ['params_market', 'plate_type', 'plate_code']")

    def params(self) -> Dict:
        """"""
        sort_by = self.params_sort_by()
        fields = self.params_fields()

        if sort_by not in fields:
            raise ValueError(f"Invalid sort_by value, please check the value in the `fields` attribute. {fields}")

        params = {
            "fid": sort_by,
            "po": self.params_ascending(),
            "pz": self.size,
            "pn": 1,
            "np": 1,
            "fltt": 2,
            "invt": 2,
            "fs": self.params_fs(),
            "fields": fields,
        }
        return params
