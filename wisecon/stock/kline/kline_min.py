from typing import Any, Dict, Callable, Optional, Literal
from wisecon.types import BaseMapping, APIStockTrends2


__all__ = [
    "KlineMinMapping",
    "KlineMin",
]


class KlineMinMapping(BaseMapping):
    """字段映射 股票-KlineMin"""
    columns: Dict = {
        "time": "时间",
        "open": "开盘",
        "close": "收盘",
        "high": "最高",
        "low": "最低",
        "volume": "成交量",
        "turnover": "成交额",
        "unknown": "unknown",
    }


class KlineMin(APIStockTrends2):
    """查询 股票-KlineMin，可以获取最大近5天的分钟级K线数据"""
    def __init__(
            self,
            security_code: Optional[str] = None,
            plate_code: Optional[str] = None,
            n_days: Optional[int] = 1,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        """
        Notes:
            ```python
            from wisecon.stock.kline import *

            # 1. 查询股票的 K线数据
            data = KlineMin(security_code="300069", n_days=1).load()
            data.to_frame(chinese_column=True)

            # 2. 查询板块的 K线数据
            data = KlineMin(plate_code="BK0887", n_days=1).load()
            print(data.to_markdown(chinese_column=True))
            ```

        Args:
            security_code: 股票代码
            plate_code: 板块代码
            n_days: 查询天数
            verbose: 是否打印日志
            logger: 日志对象
            **kwargs: 其他参数
        """
        self.security_code = security_code
        self.plate_code = plate_code
        self.n_days = n_days
        self.mapping = KlineMinMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs
        self.request_set(description="股票-KlineMin")
        self.validate_n_days()

    def validate_n_days(self):
        """"""
        if self.n_days > 5:
            raise ValueError("n_days should be less than or equal to 5")

    def params_secid(self) -> str:
        """"""
        if self.security_code:
            return f"0.{self.security_code}"
        elif self.plate_code:
            return f"90.{self.plate_code}"

    def params(self) -> Dict:
        """
        :return:
        """
        params = {
            "ndays": self.n_days,
            "secid": self.params_secid(),
        }
        return self.base_param(update=params)
