from typing import Any, Dict, Callable, Optional, Literal
from wisecon.types import BaseMapping, APIDataV1RequestData


__all__ = [
    "MarginTradingAccountMapping",
    "MarginTradingAccount",
]


class MarginTradingAccountMapping(BaseMapping):
    """字段映射 融资融券账户统计-两融账户信息"""
    columns: Dict = {
        "STATISTICS_DATE": "统计日期",
        "DATE_MARK": "日期标识",
        "TARGET_SECURITY_NUM": "目标证券数量",
        "FIN_BUY_AMT": "融资买入金额",
        "LOAN_SELL_AMT": "借入卖出金额",
        "MARGIN_TRADE_AMT": "保证金交易金额",
        "FIN_BALANCE": "融资余额",
        "LOAN_BALANCE": "借入余额",
        "MARGIN_BALANCE": "保证金余额",
        "SECURITY_ORG_NUM": "证券机构数量",
        "OPERATEDEPT_NUM": "操作部门数量",
        "END_ACC_NUM": "账户总数",
        "ADD_ACC_NUM": "新增账户数量",
        "FUND_MARKET_CAP": "基金市场总值",
        "STOCK_MARKET_CAP": "股票市场总值",
        "OTHER_MARKET_CAP": "其他市场总值",
        "TOTAL_MARKET_CAP": "市场总值",
        "TOTAL_GUARANTEE": "总保证金",
        "AVG_GUARANTEE_RATIO": "平均保证金比例",
        "SCI_CLOSE_PRICE": "SCI收盘价",
        "SCI_CHANGE_RATE": "SCI变动率",
        "ADD_ACC_RATIO": "新增账户比例",
        "BALANCE_RATIO": "余额比例",
        "TRADE_AMT_RATIO": "交易金额比例",
        "PERSONAL_INVESTOR_NUM": "个人投资者数量",
        "ORG_INVESTOR_NUM": "机构投资者数量",
        "INVESTOR_NUM": "投资者总数",
        "MARGINLIAB_INVESTOR_NUM": "保证金负债投资者数量",
        "SUBSITUTION__CAP": "替代资本"
    }


class MarginTradingAccount(APIDataV1RequestData):
    """查询 融资融券账户统计-两融账户信息"""
    def __init__(
            self,
            cycle: Literal["day", "month"] = "day",
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

            # 查询 融资融券账户统计-两融账户信息
            data = MarginTradingAccount(market="全部").load()
            data.to_frame(chinese_column=True)
            ```

        Args:
            cycle: 统计周期
            start_date: 开始日期
            end_date: 结束日期
            date: 日期
            size: 返回数据量
            verbose: 是否打印日志
            logger: 自定义日志打印函数
            **kwargs: 其他参数
        """
        self.cycle = cycle
        self.start_date = start_date
        self.end_date = end_date
        self.date = date
        self.size = size
        self.mapping = MarginTradingAccountMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs
        self.request_set(description="融资融券账户统计-两融账户信息")
        self.conditions = []
        self.validate_date_format(date=[date, start_date, end_date])

    def params_report_name(self) -> str:
        """"""
        if self.cycle == "day":
            return "RPTA_WEB_MARGIN_DAILYTRADE"
        else:
            return "RPTA_WEB_MARGIN_MONTHTRADE"

    def params_filter(self) -> str:
        """"""
        self.filter_report_date(date_name="STATISTICS_DATE")
        return "".join(self.conditions)

    def params(self) -> Dict:
        """"""
        params = {
            "reportName": self.params_report_name(),
            "sortColumns": "STATISTICS_DATE",
            "sortTypes": "-1",
            "pageSize": self.size,
            "filter": self.params_filter(),
            "pageNo": "1",
        }
        return self.base_param(update=params)
