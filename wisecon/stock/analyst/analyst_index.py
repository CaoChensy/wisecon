from typing import Any, Dict, Callable, Optional
from wisecon.types import BaseMapping, APIAnalystInvest


__all__ = [
    "AnalystIndexMapping",
    "AnalystIndex",
]


class AnalystIndexMapping(BaseMapping):
    """字段映射 分析师指数"""
    columns: Dict = {
        "ANALYST_CODE": "分析师代码",
        "ANALYST_NAME": "分析师姓名",
        "ORG_CODE": "机构代码",
        "ORG_NAME": "机构名称",
        "INDEX_PVALUE": "指数基准值",
        "INDEX_VALUE": "指数值",
        "TRADE_DATE": "交易日期",
        "UPDATE_DATE": "更新时间",
        "INDEX_HVALUE": "指数历史值",
        "INDEX_CHANGE": "指数变动",
        "INDEX_CHANGE_RATE": "指数变动率"
    }


class AnalystIndex(APIAnalystInvest):
    """查询 分析师指数"""
    def __init__(
            self,
            analyst_code: Optional[str] = None,
            size: Optional[int] = 100,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        """
        Notes:
            ```python
            from wisecon.stock.analyst import *

            data = AnalystIndex(analyst_code="11000280036").load()
            print(data.to_markdown(chinese_column=True))
            ```

        Args:
            analyst_code: 分析师代码
            size: 返回数据量
            verbose: 是否打印日志
            logger: 自定义日志打印函数
            **kwargs: 其他参数
        """
        self.analyst_code = analyst_code
        self.size = size
        self.mapping = AnalystIndexMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs
        self.request_set(description="分析师指数")
        self.conditions = []

    def params_filter(self) -> str:
        """"""
        self.conditions.append(f'(ANALYST_CODE="{self.analyst_code}")')
        return "".join(self.conditions)

    def params(self) -> Dict:
        """"""
        params = {
            "sortColumns": "TRADE_DATE",
            "sortTypes": "-1",
            "pageSize": self.size,
            "reportName": "RPT_RESEARCHER_DETAILS",
            "filter": self.params_filter(),
        }
        return self.base_param(update=params)
