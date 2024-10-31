from typing import Any, Dict, Callable, Optional, Literal
from wisecon.types import BaseMapping, APIDataV1RequestData


__all__ = [
    "MarginTradingSummaryMapping",
    "MarginTradingSummary",
]


class MarginTradingSummaryMapping(BaseMapping):
    """字段映射 融资融券交易总量-市场合计"""
    columns: Dict = {
        "RZYE": "融资余额",
        "RQYL": "融券余额",
        "RZMRE": "融资买入额",
        "DIM_DATE": "日期",
        "XOB_MARKET_0001": "市场",
        "RQYE": "融券余量",
        "SCDM": "市场代码",
        "RQMCL": "融券卖出量",
        "NEW": "新增",
        "ZDF": "涨跌幅",
        "LTSZ": "流通市值",
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
        "ZDF3D": "3日涨跌幅",
        "ZDF5D": "5日涨跌幅",
        "ZDF10D": "10日涨跌幅",
        "RZRQYE": "融资融券余额",
        "RZRQYECZ": "融资融券余额调整",
    }


class MarginTradingSummary(APIDataV1RequestData):
    """查询 融资融券交易总量-市场合计"""
    def __init__(
            self,
            market: Literal["全部", "沪市", "深市", "京市"] = "全部",
            start_date: Optional[str] = None,
            end_date: Optional[str] = None,
            date: Optional[str] = None,
            size: Optional[int] = 100,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        """
        Notes:
            ```python
            from wisecon.stock.margin import *

            # 查询 融资融券交易总量-市场合计
            data = MarginTradingSummary(market="全部").load()
            data.to_frame(chinese_column=True)
            ```

        Args:
            market: 市场类型
            start_date: 开始日期
            end_date: 结束日期
            date: 日期
            size: 返回数据量
            verbose: 是否打印日志
            logger: 自定义日志打印函数
            **kwargs: 其他参数
        """
        self.market = market
        self.start_date = start_date
        self.end_date = end_date
        self.date = date
        self.size = size
        self.mapping = MarginTradingSummaryMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs
        self.request_set(description="融资融券交易总量-市场合计")
        self.conditions = []

    def params_report_name(self) -> str:
        """"""
        if self.market == "全部":
            return "RPTA_RZRQ_LSHJ"
        else:
            return "RPTA_WEB_RZRQ_LSSH"

    def params_filter(self) -> str:
        """"""
        self.filter_report_date(date_name="DIM_DATE")
        market_mapping = {
            "沪市": "007", "深市": "001", "京市": "002"
        }
        if self.market in market_mapping:
            self.conditions.append(f'(scdm="{market_mapping[self.market]}")')
        return "".join(self.conditions)

    def params(self) -> Dict:
        """"""
        params = {
            "reportName": self.params_report_name(),
            "sortColumns": "dim_date",
            "sortTypes": "-1",
            "pageSize": self.size,
            "filter": self.params_filter(),
            "pageNo": "1",
        }
        return self.base_param(update=params)
