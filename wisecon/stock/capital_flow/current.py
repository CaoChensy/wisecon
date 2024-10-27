from typing import Any, List, Dict, Union, Callable, Optional
from .base import CapitalFlowCurrentBaseMapping, CapitalFlowCurrentRequestData

__all__ = [
    "CapitalFlowCurrentMapping",
    "CapitalFlowCurrent",
]


class CapitalFlowCurrentMapping(CapitalFlowCurrentBaseMapping):
    """字段映射 当前股票资金流量统计"""


class CapitalFlowCurrent(CapitalFlowCurrentRequestData):
    """查询 当前股票资金流量统计，最多可以同步查询10条，超过10条请使用 `StockFlow` 方法。"""
    def __init__(
            self,
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
            ```

        Args:
            security_code: 股票代码
            size: 数据条数
            verbose: 是否显示日志
            logger: 日志记录器
            **kwargs: 其他参数
        """
        self.security_code = security_code
        self.size = size
        self.mapping = CapitalFlowCurrentMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs
        self.request_set(description="当前股票资金流量统计", )

    def validate_security_code(self) -> None:
        """"""
        if isinstance(self.security_code, list) and len(self.security_code) > 10:
            raise ValueError("security_code maximum length is 10.")

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

    def params(self) -> Dict:
        """
        :return:
        """
        params = {"secids": self.params_security_code()}
        return self.base_param(update=params)
