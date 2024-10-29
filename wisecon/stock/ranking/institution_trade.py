from typing import Any, Dict, Optional, Callable
from wisecon.types import APIDataV1RequestData, BaseMapping


__all__ = [
    "InstitutionTradeRankMapping",
    "InstitutionTradeRank",
]


class InstitutionTradeRankMapping(BaseMapping):
    """字段映射 机构买卖每日统计"""
    columns: Dict = {
        "SECUCODE": "证券代码",
        "SECURITY_NAME_ABBR": "证券简称",
        "SECURITY_CODE": "证券代码",
        "TRADE_DATE": "交易日期",
        "CLOSE_PRICE": "收盘价格",
        "CHANGE_RATE": "变动率",
        "BUY_TIMES": "买入次数",
        "SELL_TIMES": "卖出次数",
        "BUY_AMT": "买入金额",
        "SELL_AMT": "卖出金额",
        "NET_BUY_AMT": "净买入金额",
        "ACCUM_AMOUNT": "累计金额",
        "RATIO": "比例",
        "TURNOVERRATE": "换手率",
        "FREECAP": "自由流通市值",
        "EXPLANATION": "说明",
        "D1_CLOSE_ADJCHRATE": "D1日收盘调整幅度",
        "D2_CLOSE_ADJCHRATE": "D2日收盘调整幅度",
        "D3_CLOSE_ADJCHRATE": "D3日收盘调整幅度",
        "D5_CLOSE_ADJCHRATE": "D5日收盘调整幅度",
        "D10_CLOSE_ADJCHRATE": "D10日收盘调整幅度",
        "MARKET": "市场",
        "TRADE_MARKET_CODE": "交易市场代码",
        "BUY_COUNT": "买入计数",
        "SELL_COUNT": "卖出计数",
        "SECURITY_TYPE_CODE": "证券类型代码"
    }


class InstitutionTradeRank(APIDataV1RequestData):
    """查询 机构买卖每日统计"""

    def __init__(
            self,
            start_date: Optional[str] = None,
            end_date: Optional[str] = None,
            size: Optional[int] = 20,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        """
        Notes:
            ```python
            from wisecon.stock.ranking import *

            data = InstitutionTradeRank(start_date="2024-10-23").load()
            data.to_frame(chinese_column=True)
            ```

        Args:
            start_date: 开始日期
            end_date: 结束日期
            size: 数据条数
            verbose: 是否打印日志
            logger: 日志记录器
            **kwargs: 其他参数
        """
        self.start_date = start_date
        self.end_date = end_date
        self.size = size
        self.mapping = InstitutionTradeRankMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs
        self.request_set(description="机构买卖每日统计",)
        self.conditions = []
        self.validate_date_format(date=[start_date, end_date], _format="%Y-%m-%d")

    def params_filter(self) -> str:
        """"""
        self.filter_report_date(date_name="TRADE_DATE")
        return "".join(self.conditions)

    def params(self) -> Dict:
        """
        :return:
        """
        params = {
            "filter": self.params_filter(),
            "pageSize": self.size,
            "sortColumns": "NET_BUY_AMT,TRADE_DATE,SECURITY_CODE",
            "sortTypes": "-1,-1,1",
            "reportName": "RPT_ORGANIZATION_TRADE_DETAILSNEW",
        }
        return self.base_param(update=params)
