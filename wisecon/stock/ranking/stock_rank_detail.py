from typing import Any, Dict, Optional, Literal, Callable
from wisecon.types import APIDataV1RequestData, BaseMapping


__all__ = [
    "StockRankDetailMapping",
    "StockRankDetail",
]


class StockRankDetailMapping(BaseMapping):
    """字段映射 个股上榜统计"""
    columns: Dict = {
        "SECURITY_CODE": "证券代码",
        "SECUCODE": "证券代码",
        "SECURITY_NAME_ABBR": "证券简称",
        "TRADE_DATE": "交易日期",
        "EXPLAIN": "说明",
        "CLOSE_PRICE": "收盘价格",
        "CHANGE_RATE": "变动率",
        "BILLBOARD_NET_AMT": "排行榜净金额",
        "BILLBOARD_BUY_AMT": "排行榜买入金额",
        "BILLBOARD_SELL_AMT": "排行榜卖出金额",
        "BILLBOARD_DEAL_AMT": "排行榜成交金额",
        "ACCUM_AMOUNT": "累计金额",
        "DEAL_NET_RATIO": "成交净比率",
        "DEAL_AMOUNT_RATIO": "成交金额比率",
        "TURNOVERRATE": "换手率",
        "FREE_MARKET_CAP": "自由流通市值",
        "EXPLANATION": "解释",
        "D1_CLOSE_ADJCHRATE": "D1日收盘调整幅度",
        "D2_CLOSE_ADJCHRATE": "D2日收盘调整幅度",
        "D5_CLOSE_ADJCHRATE": "D5日收盘调整幅度",
        "D10_CLOSE_ADJCHRATE": "D10日收盘调整幅度",
        "SECURITY_TYPE_CODE": "证券类型代码"
    }


class StockRankDetail(APIDataV1RequestData):
    """查询 个股上榜统计"""

    def __init__(
            self,
            market: Optional[Literal["沪市A股", "科创板", "深市A股", "创业板", "京市A股"]] = None,
            start_date: Optional[str] = None,
            end_date: Optional[str] = None,
            date: Optional[str] = None,
            size: Optional[int] = 20,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        """
        Notes:
            ```python
            from wisecon.stock.ranking import *

            data = StockRankDetail().load()
            data.to_frame(chinese_column=True)
            ```

        Args:
            market: 市场类型, 可选值: 沪市A股, 科创板, 深市A股, 创业板, 京市A股, 默认值: None
            start_date: 开始日期, 格式: yyyy-MM-dd, 默认值: None
            end_date: 结束日期, 格式: yyyy-MM-dd, 默认值: None
            date: 日期, 格式: yyyy-MM-dd, 默认值: None
            size: 数据条数
            verbose: 是否打印日志
            logger: 日志记录器
            **kwargs: 其他参数
        """
        self.market = market
        self.start_date = start_date
        self.end_date = end_date
        self.date = date
        self.size = size
        self.mapping = StockRankDetailMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs
        self.request_set(description="龙虎榜详情",)
        self.conditions = []
        self.validate_date_format(date=[date, start_date, end_date])

    def params_market(self):
        """"""
        market_mapping = {
            "沪市A股": '(TRADE_MARKET_CODE in ("069001001001","069001001006","069001001003"))',
            "科创板": '(TRADE_MARKET_CODE="069001001006")',
            "深市A股": '(TRADE_MARKET_CODE in ("069001002001","069001002002","069001002005"))',
            "创业板": '(TRADE_MARKET_CODE="069001002002")',
            "京市A股": '(TRADE_MARKET_CODE="069001017")',
        }
        if self.market:
            self.conditions.append(market_mapping.get(self.market))

    def params_filter(self) -> str:
        """"""
        self.params_market()
        self.filter_report_date(date_name="TRADE_DATE")
        return "".join(self.conditions)

    def params(self) -> Dict:
        """
        :return:
        """
        columns = [
            "SECURITY_CODE", "SECUCODE", "SECURITY_NAME_ABBR", "TRADE_DATE", "EXPLAIN",
            "CLOSE_PRICE", "CHANGE_RATE", "BILLBOARD_NET_AMT", "BILLBOARD_BUY_AMT",
            "BILLBOARD_SELL_AMT", "BILLBOARD_DEAL_AMT", "ACCUM_AMOUNT", "DEAL_NET_RATIO",
            "DEAL_AMOUNT_RATIO", "TURNOVERRATE", "FREE_MARKET_CAP", "EXPLANATION", "D1_CLOSE_ADJCHRATE",
            "D2_CLOSE_ADJCHRATE", "D5_CLOSE_ADJCHRATE", "D10_CLOSE_ADJCHRATE", "SECURITY_TYPE_CODE"
        ]

        params = {
            "columns": ",".join(columns),
            "filter": self.params_filter(),
            "pageSize": self.size,
            "sortColumns": "SECURITY_CODE,TRADE_DATE",
            "sortTypes": "1,-1",
            "reportName": "RPT_DAILYBILLBOARD_DETAILSNEW",
        }
        return self.base_param(update=params)
