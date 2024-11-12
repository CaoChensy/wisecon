from typing import Any, Dict, Literal, Callable, Optional
from wisecon.types import BaseMapping, APIStockFFlowKLineRequestData


__all__ = [
    "CapitalFlowMinutesMapping",
    "CapitalFlowMinutes",
]


TypeMarket = Literal["沪深两市", "沪市", "深市", "创业板", "沪B", "深B"]


class CapitalFlowMinutesMapping(BaseMapping):
    """字段映射 市场、板块（行业、概念、地区）分钟级资金流向数据"""
    columns: Dict = {
        "TRADE_DATE": "时间",
        "main_inflow": "主力净流入",
        "small_inflow": "小单净流入",
        "medium_inflow": "中单净流入",
        "large_inflow": "大单净流入",
        "block_inflow": "超大单净流入",
    }


class CapitalFlowMinutes(APIStockFFlowKLineRequestData):
    """查询 市场、板块（行业、概念、地区）分钟级资金流向数据

    1. 查询市场总体资金流量
    2. 查询全部 `行业、地区、概念` 板块资金流量
    3. 查询指定板块资金流量
    4. 查询不同行业、地区、概念板块下的主力流入流出排名

    Notes:
        ```markdown
        指标定义
        　　- 超大单：大于等于50万股或者100万元的成交单;
        　　- 大单：大于等于10万股或者20万元且小于50万股和100万元的成交单;
        　　- 中单：大于等于2万股或者4万元且小于10万股和20万元的成交单;
        　　- 小单：小于2万股和4万元的成交单;
        ```
    """
    def __init__(
            self,
            market: Optional[TypeMarket] = None,
            plate_code: Optional[str] = None,
            security_code: Optional[str] = None,
            size: Optional[int] = 0,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        """
        Notes:
            ```python
            from wisecon.stock.capital_flow import *

            # 1. 查询市场的资金分钟流向数据
            data = CapitalFlowMinutes(market="沪深两市", size=10).load()
            data.to_frame(chinese_column=True)

            # 2.1 查询板块的资金分钟流向数据(概念)
            data = CapitalFlowMinutes(plate_code="BK1044", size=10).load()
            data.to_frame(chinese_column=True)

            # 2.2 查询板块的资金分钟流向数据(地区)
            data = CapitalFlowMinutes(plate_code="BK0158", size=10).load()
            data.to_frame(chinese_column=True)

            # 2.3 查询板块的资金分钟流向数据(行业)
            data = CapitalFlowMinutes(plate_code="BK1044", size=10).load()
            data.to_frame(chinese_column=True)

            # 3. 查询股票的资金分钟流向数据
            data = CapitalFlowMinutes(security_code="300750", size=10).load()
            data.to_frame(chinese_column=True)
            ```

        Args:
            market: 市场名称: `["沪深两市", "沪市", "深市", "创业板", "沪B", "深B"]`
            plate_code: 板块代码, 支持地区板块、行业板块、概念板块
            security_code: 股票代码
            size: 数据条数
            verbose: 是否打印日志
            logger: 自定义日志函数
            **kwargs: 其他参数
        """
        self.market = market
        self.plate_code = plate_code
        self.security_code = security_code
        self.size = size
        self.mapping = CapitalFlowMinutesMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs
        self.request_set(description="市场、板块（行业、概念、地区）分钟级资金流向数据", )
    
    def params_market_code(self) -> Dict:
        """"""
        market_mapping = {
            "沪深两市": "1.000001,0.399001", "沪市": "1.000001", "深市": "0.399001", "创业板": "0.399006", "沪B": "1.000003", "深B": "0.399003"
        }
        if self.market in market_mapping:
            if self.market == "沪深两市":
                secid, secid2 = market_mapping["沪深两市"].split(",")
                return {"secid": secid, "secid2": secid2}
            else:
                return {"secid": market_mapping[self.market]}
        else:
            raise ValueError(
                f'market error {self.market} not in ["沪深两市", "沪市", "深市", "创业板", "沪B", "深B"]')

    def params_plate_code(self) -> Dict:
        """"""
        return {"secid": f"90.{self.plate_code}"}

    def params_security_code(self) -> Dict:
        """"""
        return {"secid": f"0.{self.security_code}"}
    
    def params_secid(self) -> Dict:
        """"""
        if self.market:
            return self.params_market_code()
        elif self.plate_code:
            return self.params_plate_code()
        elif self.security_code:
            return self.params_security_code()
        else:
            raise ValueError("market_code or plate_code must be set")

    def params(self) -> Dict:
        """"""
        param_sec_id = self.params_secid()
        params = {
            "klt": "1",
            "lmt": self.size,
            "fields1": "f1,f2,f3,f7",
            "fields2": "f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61,f62,f63,f64,f65",
        }
        params.update(param_sec_id)
        return self.base_param(update=params)
