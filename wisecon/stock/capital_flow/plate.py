from typing import Any, Dict, Literal, Callable, Optional
from .base import CapitalFlowRequestData, CapitalFlowMapping


__all__ = [
    "PlateFlowMapping",
    "PlateFlow",
]


class PlateFlowMapping(CapitalFlowMapping):
    """字段映射 板块（行业、概念、地区）资金流向历史数据"""


class PlateFlow(CapitalFlowRequestData):
    """查询 板块（行业、概念、地区）资金流向历史数据

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
            plate: Optional[Literal["行业", "概念", "地区"]] = "行业",
            size: Optional[int] = 50,
            sort_by: Optional[str] = None,
            days: Optional[Literal[1, 3, 5, 10]] = 1,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        """
        Notes:
            ```python
            from wisecon.stock.capital_flow import *

            data = PlateFlow(days=1).load()
            data.to_frame(chinese_column=True)
            ```

        Args:
            plate: 板块名称, `["行业", "概念", "地区"]`
            days: 统计天数 `1, 3, 5, 10`
            size: 返回数据量
            sort_by: 排序字段名称, 可通过`StockFlowMapping`查询
            verbose: 是否打印日志
            logger: 自定义日志函数
            **kwargs: 其他参数
        """
        self.plate = plate
        self.size = size
        self.sort_by = sort_by
        self.days = days
        self.mapping = PlateFlowMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs
        self.request_set(description="板块（行业、概念、地区）资金流向历史数据", )

    def params_plate(self) -> str:
        """"""
        plate_mapping = {
            "行业": "m:90+t:2",
            "概念": "m:90+t:3",
            "地区": "m:90+t:1",
        }
        if self.plate in plate_mapping:
            return plate_mapping[self.plate]
        else:
            return plate_mapping["行业"]

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
            "fs": self.params_plate(),
            "fields": fields,
        }
        return params
