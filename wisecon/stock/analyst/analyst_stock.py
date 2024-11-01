from typing import Any, Dict, Callable, Optional
from wisecon.types import BaseMapping, APIAnalystInvest


__all__ = [
    "ResearcherStockMapping",
    "ResearcherStock",
]


class ResearcherStockMapping(BaseMapping):
    """字段映射 分析师持股"""
    columns: Dict = {
        "RATING_DATE": "评级日期",
        "TRADE_MARKET_CODE": "交易市场代码",
        "ANALYST_CODE": "分析师代码",
        "ANALYST_NAME": "分析师姓名",
        "TRADE_DATE": "交易日期",
        "SECURITY_CODE": "证券代码",
        "SECUCODE": "证券代码",
        "SECURITY_NAME_ABBR": "证券简称",
        "CHANGE_DATE": "变更日期",
        "RATING_NAME": "评级名称",
        "CLOSE_FORWARD_ADJPRICE": "收盘前调整价格",
        "NEW_PRICE": "最新价格",
        "CURRENT_CHANGE": "当前变动",
        # history
        "BFCHANGE_DATE": "之前变更日期",
        "REASON": "变更原因",
        "CHANGE_RATE": "变更幅度"
    }


class ResearcherStock(APIAnalystInvest):
    """查询 分析师持股"""
    def __init__(
            self,
            analyst_code: Optional[str] = None,
            current: Optional[bool] = True,
            size: Optional[int] = 100,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        """
        Notes:
            ```python
            from wisecon.stock.analyst import *

            # 查询当前数据
            data = ResearcherStock(analyst_code="11000280036", current=True).load()
            print(data.to_markdown(chinese_column=True))

            # 查询历史数据
            data = ResearcherStock(analyst_code="11000280036", current=False).load()
            print(data.to_markdown(chinese_column=True))
            ```

        Args:
            analyst_code: 分析师代码
            current: 是否当前持股
            size: 返回数据量
            verbose: 是否打印日志
            logger: 自定义日志打印函数
            **kwargs: 其他参数
        """
        self.analyst_code = analyst_code
        self.current = current
        self.size = size
        self.mapping = ResearcherStockMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs
        self.request_set(description="分析师持股")
        self.conditions = []

    def params_filter(self) -> str:
        """"""
        self.conditions.append(f'(ANALYST_CODE="{self.analyst_code}")')
        return "".join(self.conditions)

    def params_report_name(self) -> str:
        """"""
        if self.current:
            return "RPT_RESEARCHER_NTCSTOCK"
        else:
            return "RPT_RESEARCHER_HISTORYSTOCK"

    def params(self) -> Dict:
        """"""
        params = {
            "sortColumns": "CHANGE_DATE",
            "sortTypes": "-1",
            "pageSize": self.size,
            "reportName": self.params_report_name(),
            "filter": self.params_filter(),
        }
        return self.base_param(update=params)
