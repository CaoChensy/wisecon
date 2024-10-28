from typing import Any, List, Dict, Union, Literal, Callable, Optional
from .base import CapitalFlowCurrentBaseMapping, CapitalFlowCurrentRequestData


__all__ = [
    "CapitalFlowCurrentMapping",
    "CapitalFlowCurrent",
]


TypeMarket = Literal["沪深两市", "沪市", "深市", "创业板", "沪B", "深B"]


class CapitalFlowCurrentMapping(CapitalFlowCurrentBaseMapping):
    """字段映射 当前股票资金流量统计"""


class CapitalFlowCurrent(CapitalFlowCurrentRequestData):
    """查询 当前股票资金流量统计，最多可以同步查询10条，超过10条请使用 `StockFlow` 方法。

    1. 查询沪深两市市场当前资金动向数据
    2. 查询某行业、地区、概念板块当前资金动向数据
    3. 查询具体股票的当前资金动向数据
    """
    def __init__(
            self,
            market: Optional[TypeMarket] = None,
            plate_code: Optional[Union[str, List[str]]] = None,
            security_code: Optional[Union[str, List[str]]] = None,
            size: Optional[int] = 0,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        """
        Notes:
            ```python
            from wisecon.stock.capital_flow import *

            # 1. 查询股票的资金当前流向数据
            data = CapitalFlowCurrent(security_code="300750", size=10).load()
            data.to_frame(chinese_column=True)

            # 2. 查询板块的资金当前流向数据
            data = CapitalFlowCurrent(plate_code="BK0477", size=10).load()
            data.to_frame(chinese_column=True)

            # 3. 查询市场的资金当前流向数据
            data = CapitalFlowCurrent(market="深市A股", size=10).load()
            data.to_frame(chinese_column=True)
            ```

        Args:
            market: 市场名称 `["全部股票", "沪深A股", "沪市A股", "科创板", "深市A股", "创业板", "沪市B股", "深市B股"]`
            plate_code: 板块代码, 行业、概念、地区
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
        self.mapping = CapitalFlowCurrentMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs
        self.request_set(description="当前股票资金流量统计", )
        self.validate_max_security_codes(security_code=security_code)

    def params_market_code(self) -> str:
        """"""
        market_mapping = {
            "沪深两市": "1.000001,0.399001", "沪市": "1.000001", "深市": "0.399001",
            "创业板": "0.399006", "沪B": "1.000003", "深B": "0.399003"
        }
        if self.market in market_mapping:
            return market_mapping[self.market]
        else:
            raise ValueError(
                f'market error {self.market} not in ["沪深两市", "沪市", "深市", "创业板", "沪B", "深B"]')

    def params_security_code(self) -> str:
        """"""
        if isinstance(self.security_code, str):
            self.security_code = [self.security_code]
        for i, code in enumerate(self.security_code):
            if code.startswith("3"):
                self.security_code[i] = f"0.{code}"
            else:
                self.security_code[i] = f"1.{code}"
        return ",".join(self.security_code)

    def params_plate_code(self) -> str:
        """"""
        if isinstance(self.plate_code, str):
            self.plate_code = [self.plate_code]
        return ",".join([f"90.{code}" for code in self.plate_code])

    def params_secids(self) -> str:
        """"""
        if self.market is not None:
            return self.params_market_code()
        elif self.security_code is not None:
            return self.params_security_code()
        elif self.plate_code is not None:
            return self.params_plate_code()
        else:
            raise ValueError("security_code or plate_code must be set.")

    def params(self) -> Dict:
        """
        :return:
        """
        params = {"secids": self.params_secids()}
        return self.base_param(update=params)
