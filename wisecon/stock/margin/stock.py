from typing import Any, Dict, Callable, Optional, Literal
from wisecon.types import BaseMapping, APIDataV1RequestData


__all__ = [
    "MarginTradingStockMapping",
    "MarginTradingStock",
]


class MarginTradingStockMapping(BaseMapping):
    """字段映射 融资融券交易明细-个股融资融券"""
    columns: Dict = {
        "DATE": "日期",
        "MARKET": "市场",
        "SCODE": "证券代码",
        "SECNAME": "证券名称",
        "RZYE": "融资余额",
        "RQYL": "融券余额",
        "RZRQYE": "融资融券余额",
        "RQYE": "融券余量",
        "RQMCL": "融券卖出量",
        "RZRQYECZ": "融资融券余额调整",
        "RZMRE": "融资买入额",
        "SZ": "市值",
        "RZYEZB": "融资余额占比",
        "RZMRE3D": "3日融资买入额",
        "RZMRE5D": "5日融资买入额",
        "RZMRE10D": "10日融资买入额",
        "RZCHE": "融资偿还额",
        "RZCHE3D": "3日融资偿还额",
        "RZCHE5D": "5日融资偿还额",
        "RZCHE10D": "10日融资偿还额",
        "RZJME": "融资交易额",
        "RZJME3D": "3日融资交易额",
        "RZJME5D": "5日融资交易额",
        "RZJME10D": "10日融资交易额",
        "RQMCL3D": "3日融券卖出量",
        "RQMCL5D": "5日融券卖出量",
        "RQMCL10D": "10日融券卖出量",
        "RQCHL": "融券持有量",
        "RQCHL3D": "3日融券持有量",
        "RQCHL5D": "5日融券持有量",
        "RQCHL10D": "10日融券持有量",
        "RQJMG": "融券交易量",
        "RQJMG3D": "3日融券交易量",
        "RQJMG5D": "5日融券交易量",
        "RQJMG10D": "10日融券交易量",
        "SPJ": "收盘价",
        "ZDF": "涨跌幅",
        "RCHANGE3DCP": "3日变动幅度",
        "RCHANGE5DCP": "5日变动幅度",
        "RCHANGE10DCP": "10日变动幅度",
        "KCB": "可转债",
        "TRADE_MARKET_CODE": "交易市场代码",
        "TRADE_MARKET": "交易市场",
        "FIN_BALANCE_GR": "融资余额增长率",
        "SECUCODE": "证券代码"
    }


class MarginTradingStock(APIDataV1RequestData):
    """查询 融资融券交易明细-个股融资融券"""
    def __init__(
            self,
            market: Literal["沪深A股", "沪市A股", "科创板", "深市A股", "创业板", "京市A股"] = None,
            start_date: Optional[str] = None,
            end_date: Optional[str] = None,
            date: Optional[str] = None,
            cycle: Literal[1, 3, 5, 10] = 1,
            size: Optional[int] = 50,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        """
        Notes:
            ```python
            from wisecon.stock.margin import *

            # 查询 融资融券交易明细-个股融资融券
            data = MarginTradingStock(date="2024-10-30", cycle=1).load()
            data.to_frame(chinese_column=True)

            data = MarginTradingStock(market="沪深A股", date="2024-10-30", cycle=1).load()
            data.to_frame(chinese_column=True)

            data = MarginTradingStock(market="科创板", date="2024-10-30", cycle=1).load()
            data.to_frame(chinese_column=True)
            ```

        Args:
            market: 市场名称: `["沪深A股", "沪市A股", "科创板", "深市A股", "创业板", "京市A股"]`
            start_date: 开始日期
            end_date: 结束日期
            date: 日期
            cycle: 统计周期
            size: 返回数据量
            verbose: 是否打印日志
            logger: 自定义日志打印函数
            **kwargs: 其他参数
        """
        self.market = market
        self.cycle = cycle
        self.start_date = start_date
        self.end_date = end_date
        self.date = date
        self.size = size
        self.mapping = MarginTradingStockMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs
        self.request_set(description="融资融券交易明细-个股融资融券")
        self.conditions = []
        self.validate_date_format(date=[date, start_date, end_date])

    def params_filter(self) -> str:
        """"""
        market_mapping = {
            "沪深A股": '"069001001001","069001001006","069001002001","069001002002","069001002003"',
            "沪市A股": '"069001001001","069001001006"',
            "科创板": '"069001001006"',
            "深市A股": '"069001002001","069001002002","069001002003"',
            "创业板": '"069001002002"',
            "京市A股": '"069001017"',
        }
        self.filter_report_date(date_name="DATE")
        if self.market:
            self.conditions.append(f'(TRADE_MARKET_CODE in ({market_mapping[self.market]}))')
        return "".join(self.conditions)

    def params_sort_column(self):
        """"""
        if self.cycle == 1:
            return "RZJME"
        else:
            return f"RZJME{self.cycle}D"

    def params(self) -> Dict:
        """"""
        params = {
            "reportName": "RPTA_WEB_RZRQ_GGMX",
            "sortColumns": self.params_sort_column(),
            "sortTypes": "-1",
            "pageSize": self.size,
            "filter": self.params_filter(),
            "pageNo": "1",
        }
        return self.base_param(update=params)
