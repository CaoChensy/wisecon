from typing import Any, Dict, Literal, Callable, Optional
from .base import CapitalFlowHistoryBaseMapping, CapitalFlowHistoryRequestData

__all__ = [
    "CapitalFlowHistoryMapping",
    "CapitalFlowHistory",
]


TypeMarket = Literal["沪深两市", "沪市", "深市", "创业板", "沪B", "深B"]


class CapitalFlowHistoryMapping(CapitalFlowHistoryBaseMapping):
    """字段映射 资金流向历史数据(大盘沪深两市/板块历史数据)"""


class CapitalFlowHistory(CapitalFlowHistoryRequestData):
    """查询 资金流向历史数据(大盘沪深两市/板块历史数据)

    1. 查询沪深两市市场历史资金动向数据
    2. 查询某行业、地区、概念板块历史资金动向数据
    3. 查询具体股票的历史资金动向数据
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

            # 1. 查询市场的资金历史流向数据
            data = CapitalFlowHistory(market="沪深两市", size=10).load()
            data.to_frame(chinese_column=True)

            # 2.1 查询板块的资金历史流向数据(概念)
            data = CapitalFlowHistory(plate_code="BK1044", size=10).load()
            data.to_frame(chinese_column=True)

            # 2.2 查询板块的资金历史流向数据(地区)
            data = CapitalFlowHistory(plate_code="BK0158", size=10).load()
            data.to_frame(chinese_column=True)

            # 2.3 查询板块的资金历史流向数据(行业)
            data = CapitalFlowHistory(plate_code="BK1044", size=10).load()
            data.to_frame(chinese_column=True)

            # 3. 查询股票的资金历史流向数据
            data = CapitalFlowHistory(security_code="300750", size=10).load()
            data.to_frame(chinese_column=True)
            ```

        Args:
            market: 市场名称: `["沪深两市", "沪市", "深市", "创业板", "沪B", "深B"]`
            plate_code: 板块代码, 支持地区板块、行业板块、概念板块
            security_code: 股票代码
            size: 数据条数
            verbose: 是否显示日志
            logger: 日志记录器
            **kwargs: 其他参数
        """
        self.market = market
        self.plate_code = plate_code
        self.security_code = security_code
        self.size = size
        self.mapping = CapitalFlowHistoryMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs
        self.request_set(description="资金流向历史数据(大盘沪深两市/板块历史数据)", )

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
        """
        :return:
        """
        param_sec_id = self.params_secid()
        params = {"lmt": self.size, }
        params.update(param_sec_id)
        return self.base_param(update=params)
