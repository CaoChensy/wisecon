from typing import Any, Dict, Callable, Optional
from wisecon.types import BaseMapping, APIDataV1RequestData


__all__ = [
    "StockDividend",
    "StockDividendMapping",
]


class StockDividendMapping(BaseMapping):
    """字段映射 上市公司分红数据"""
    columns: Dict = {
        "SECUCODE": "证券代码",
        "SECURITY_NAME_ABBR": "证券简称",
        "SECURITY_INNER_CODE": "内部代码",
        "ORG_CODE": "机构代码",
        "SECURITY_CODE": "证券代码",
        "BONUS_IT_RATIO": "股息税后比例",
        "BONUS_RATIO": "股息比例",
        "IT_RATIO": "分配比例",
        "PRETAX_BONUS_RMB": "税前股息（人民币）",
        "PLAN_NOTICE_DATE": "计划通知日期",
        "EQUITY_RECORD_DATE": "股权登记日期",
        "EX_DIVIDEND_DATE": "除息日期",
        "REPORT_DATE": "报告日期",
        "ASSIGN_PROGRESS": "方案进度",
        "IMPL_PLAN_PROFILE": "现金分红比例",
        "NOTICE_DATE": "公告日期",
        "MARKET_TYPE": "市场类型",
        "EX_DIVIDEND_DAYS": "除息天数",
        "IS_KCB": "是否科创板",
        "BASIC_EPS": "每股收益(元)",
        "BVPS": "每股净资产(元)",
        "PER_CAPITAL_RESERVE": "每股公积金(元)",
        "PER_UNASSIGN_PROFIT": "每股未分配利润(元)",
        "PNP_YOY_RATIO": "净利润同比增长率(%)",
        "TOTAL_SHARES": "总股本(元)",
        "PUBLISH_DATE": "发布日期",
        "DIVIDENT_RATIO": "股息率",
        "D10_CLOSE_ADJCHRATE": "10日收盘价调整变化率",
        "BD10_CLOSE_ADJCHRATE": "前10日收盘价调整变化率",
        "D30_CLOSE_ADJCHRATE": "30日收盘价调整变化率"
    }


class StockDividend(APIDataV1RequestData):
    """查询 上市公司分红数据"""
    def __init__(
            self,
            security_code: Optional[str] = None,
            size: Optional[int] = 50,
            start_date: Optional[str] = None,
            end_date: Optional[str] = None,
            date: Optional[str] = None,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        """
        Notes:
            ```python
            from wisecon.stock.financial import StockDividend

            data = StockDividend(date="2024-09-30", size=5).load()
            data.to_frame(chinese_column=True)
            ```

        Args:
            security_code: 证券代码
            size: 数据条数据
            start_date: 开始日期
            end_date: 结束日期
            date: 指定日期
            verbose: 是否打印日志
            logger: 日志对象
            **kwargs: 其他参数
        """
        self.security_code = security_code
        self.size = size
        self.start_date = start_date
        self.end_date = end_date
        self.date = date
        self.mapping = StockDividendMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs
        self.request_set(response_type="json", description="上市公司分红数据")

    def params_filter(self) -> str:
        """"""
        conditions = []
        if self.start_date:
            conditions.append(f"(REPORT_DATE>='{self.start_date}')")
        if self.end_date:
            conditions.append(f"(REPORT_DATE<='{self.end_date}')")
        if self.date:
            conditions.append(f"(REPORT_DATE='{self.date}')")
        if self.security_code:
            conditions.append(f'(SECURITY_CODE="{self.security_code}")')
        return "".join(conditions)

    def params(self) -> Dict:
        """
        :return:
        """
        params = {
            "filter": self.params_filter(),
            "sortColumns": "PLAN_NOTICE_DATE",
            "sortTypes": -1,
            "pageSize": self.size,
            "pageNumber": 1,
            "reportName": "RPT_SHAREBONUS_DET",
        }
        return self.base_param(params)
