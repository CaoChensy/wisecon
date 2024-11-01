from typing import Any, Dict, Callable, Optional
from wisecon.types import BaseMapping, APIAnalystInvest


__all__ = [
    "AnalystYearRankMapping",
    "AnalystYearRank",
]


class AnalystYearRankMapping(BaseMapping):
    """字段映射 分析师指数-年度排行榜"""
    columns: Dict = {
        "ANALYST_CODE": "分析师代码",
        "ANALYST_NAME": "分析师姓名",
        "TRADE_DATE": "交易日期",
        "YEAR": "年份",
        "ORG_NAME": "机构名称",
        "ORG_CODE": "机构代码",
        "INDEX_VALUE": "指数值",
        "YEAR_YIELD": "年度收益率",
        "YIELD_3": "3个月收益率",
        "YIELD_6": "6个月收益率",
        "YIELD_12": "12个月收益率",
        "SECURITY_COUNT": "证券数量",
        "SECURITY_NAME_ABBR": "证券简称",
        "SECUCODE": "证券代码",
        "SECURITY_CODE": "证券代码",
        "NEWEST_STOCK_RATING": "最新股票评级",
        "INDUSTRY_CODE": "行业代码",
        "INDUSTRY_NAME": "行业名称"
    }


class AnalystYearRank(APIAnalystInvest):
    """查询 分析师指数-年度排行榜"""
    def __init__(
            self,
            year: Optional[str] = None,
            top_n: Optional[int] = None,
            industry_code: Optional[str] = None,
            size: Optional[int] = 50,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        """
        Notes:
            ```python
            from wisecon.stock.analyst import *
            from wisecon.stock.plate_mapping import *

            # 查询全部 2024 年度排行榜
            data = AnalystYearRank(year="2024").load()
            print(data.to_markdown(chinese_column=True))

            # 指定行业编码
            data = AnalystYearRank(year="2024", industry_code="480000").load()
            print(data.to_markdown(chinese_column=True))

            # 查询行业编码
            data = IndustryCode().load()
            print(data.to_markdown(chinese_column=True))
            ```

        Args:
            year: 年份
            top_n: 排名
            industry_code: 行业代码
            size: 返回数据量
            verbose: 是否打印日志
            logger: 自定义日志打印函数
            **kwargs: 其他参数
        """
        self.year = year
        self.top_n = top_n
        self.industry_code = industry_code
        self.size = size
        self.mapping = AnalystYearRankMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs
        self.request_set(description="分析师指数-年度排行榜")
        self.conditions = []

    def params_top_n(self) -> int:
        """"""
        if self.top_n is not None:
            return self.top_n
        else:
            if self.industry_code is not None:
                return 10
            else:
                return 100

    def params_filter(self) -> str:
        """"""
        if self.year:
            self.conditions.append(f'(YEAR="{self.year}")')
        else:
            raise ValueError("year is required.")
        if self.industry_code:
            self.conditions.append(f'(INDUSTRY_CODE="{self.industry_code}")')
        return "".join(self.conditions)

    def params(self) -> Dict:
        """"""
        params = {
            "sortColumns": "YEAR_YIELD",
            "sortTypes": "-1",
            "pageSize": self.size,
            "reportName": "RPT_ANALYST_INDEX_RANK",
            "distinct": "ANALYST_CODE",
            "limit": f"top{self.params_top_n()}",
            "filter": self.params_filter(),
        }
        return self.base_param(update=params)
