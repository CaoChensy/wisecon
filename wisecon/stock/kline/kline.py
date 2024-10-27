from typing import Any, Dict, Callable, Optional, Literal, List
from wisecon.types import BaseMapping, APIStockKline


__all__ = [
    "KLineMapping",
    "KLine",
]


TypePeriod = Literal["1min", "5min", "15min", "30min", "60min", "1day", "1week", "1month"]


class KLineMapping(BaseMapping):
    """字段映射 股票-KLine"""
    columns: Dict = {
        "open": "开盘",
        "close": "收盘",
        "high": "最高",
        "low": "最低",
        "change_pct": "涨跌幅",
        "change_amt": "涨跌额",
        "volume": "成交量",
        "turnover": "成交额",
        "amplitude": "振幅",
        "turnover_rate": "换手率"
    }


class KLine(APIStockKline):
    """查询 股票-KLine"""
    def __init__(
            self,
            code: Optional[str] = None,
            end: Optional[str] = "20500101",
            limit: Optional[int] = 120,
            period: Optional[TypePeriod] = "5min",
            adjust: Optional[Literal["前复权", "后赋权", "不赋权"]] = "前复权",
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        """
        Notes:
            ```python
            from wisecon.stock.kline import KLine

            data = KLine(code="300069", end="20240910", period="1day", limit=9).load()
            data.to_frame(chinese_column=True)
            ```

        Args:
            code: 股票代码
            end: 截止日期
            limit: 返回数据条数
            period: K线周期`["1min", "5min", "15min", "30min", "60min", "1day", "1week", "1month"]`
            adjust: 复权类型`["前复权", "后赋权", "不赋权"]`
            verbose: 是否打印日志
            logger: 日志对象
            **kwargs: 其他参数
        """
        self.code = code
        self.end = end
        self.limit = limit
        self.period = period
        self.adjust = adjust
        self.mapping = KLineMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs
        self.request_set(description="股票-KLine")

    def params_adjust_type(self) -> int:
        """"""
        adjust_mapping = {"前复权": 1, "后赋权": 2, "不赋权": 0}
        return adjust_mapping.get(self.adjust, 1)

    def params_period(self) -> str:
        """"""
        period_mapping = {
            "1min": "1", "5min": "5", "15min": "15", "30min": "30", "60min": "60",
            "1day": "101", "1week": "102", "1month": "103"
        }
        return period_mapping.get(self.period, "5")

    def params(self) -> Dict:
        """
        :return:
        """
        params = {
            "secid": f"0.{self.code}",
            "fields1": "f1,f2,f3,f4,f5,f6",
            "fields2": "f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61",
            "klt": self.params_period(),
            "fqt": self.params_adjust_type(),
            "end": self.end,
            "lmt": self.limit,
        }
        return params
