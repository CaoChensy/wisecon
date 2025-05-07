from typing import Any, Dict, Callable, Optional, Literal, Annotated
from wisecon.types import BaseMapping, APIStockKline


__all__ = [
    "KLineMapping",
    "KLine",
]


class KLineMapping(BaseMapping):
    """字段映射 股票-KLine"""
    columns: Dict = {
        "time": "时间",
        "open": "开盘",
        "close": "收盘",
        "high": "最高",
        "low": "最低",
        "volume": "成交量",
        "turnover": "成交额",
        "amplitude": "振幅",
        "change_pct": "涨跌幅",
        "change_amt": "涨跌额",
        "turnover_rate": "换手率"
    }


class KLine(APIStockKline):
    """查询 股票-KLine

    注意：非交易日时，1分钟线`1m`无数据。
    """
    def __init__(
            self,
            market_code: Annotated[Optional[str], "市场代码", False] = None,
            security_code: Annotated[Optional[str], "证券代码", False] = None,
            plate_code: Annotated[Optional[str], "板块代码", False] = None,
            end_date: Annotated[Optional[str], "开始时间", False] = "20500101",
            size: Annotated[Optional[int], "返回数据条数", False] = 120,
            period: Annotated[Literal["1m", "5m", "15m", "30m", "60m", "1D", "1W", "1M"], "", False] = "5m",
            adjust: Annotated[Literal["前复权", "后赋权", "不赋权"], "", False] = "前复权",
            verbose: Annotated[Optional[bool], "是否显示日志", False] = False,
            logger: Annotated[Optional[Callable], "日志对象", False] = None,
            **kwargs: Annotated[Any, "其他参数", False]
    ):
        """
        Notes:
            ```python
            from wisecon.stock.kline import *

            # 0. 查询沪深300 K线数据
            data = KLine(market_code="000300", period="1D", size=5).load()
            data.to_frame(chinese_column=True)

            # 1. 查询股票的 K线数据
            data = KLine(security_code="300069", period="1D", size=5).load()
            data.to_frame(chinese_column=True)

            # 2. 查询板块的 K线数据
            data = KLine(plate_code="BK0887", period="1D", size=5).load()
            print(data.to_markdown(chinese_column=True))
            ```

        Args:
            market_code: 市场代码
            security_code: 股票代码
            plate_code: 板块代码
            end_date: 截止日期
            size: 返回数据条数
            period: K线周期`["1m", "5m", "15m", "30m", "60m", "1D", "1W", "1M"]`
            adjust: 复权类型`["前复权", "后赋权", "不赋权"]`
            verbose: 是否打印日志
            logger: 日志对象
            **kwargs: 其他参数
        """
        self.market_code = market_code
        self.security_code = security_code
        self.plate_code = plate_code
        self.end_date = end_date
        self.size = size
        self.period = period
        self.adjust = adjust
        self.mapping = KLineMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs
        self.request_set(description="股票-KLine")
        self.validate_date_format(date=end_date, _format="%Y%m%d")

    def params_adjust_type(self) -> int:
        """"""
        adjust_mapping = {"前复权": 1, "后赋权": 2, "不赋权": 0}
        return adjust_mapping[self.adjust]

    def params_period(self) -> str:
        """"""
        period_mapping = {
            "1m": "1", "5m": "5", "15m": "15", "30m": "30", "60m": "60",
            "1D": "101", "1W": "102", "1M": "103"
        }
        return period_mapping[self.period]

    def params_secid(self) -> str:
        """"""
        if self.market_code:
            return f"1.{self.market_code}"
        elif self.security_code:
            if self.security_code.startswith("6"):
                return f"1.{self.security_code}"
            else:
                return f"0.{self.security_code}"
        elif self.plate_code:
            return f"90.{self.plate_code}"

    def params(self) -> Dict:
        """
        :return:
        """
        params = {
            "secid": self.params_secid(),
            "fields1": "f1,f2,f3,f4,f5,f6",
            "fields2": "f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61",
            "klt": self.params_period(),
            "fqt": self.params_adjust_type(),
            "end": self.end_date,
            "lmt": self.size,
        }
        return params
