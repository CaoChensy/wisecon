from typing import Any, Dict, Callable, Optional
from wisecon.types import BaseMapping, APIDataV1RequestData


__all__ = [
    "ScheduledDisclosure",
    "ScheduledDisclosureMapping",
]


class ScheduledDisclosureMapping(BaseMapping):
    """字段映射 上市公司预约披露时间"""
    columns: Dict = {
        "SECURITY_CODE": "证券代码",
        "SECURITY_NAME_ABBR": "证券简称",
        "REPORT_TYPE": "报告类型",
        "REPORT_YEAR": "报告年份",
        "FIRST_APPOINT_DATE": "首次任命日期",
        "FIRST_CHANGE_DATE": "首次变更日期",
        "SECOND_CHANGE_DATE": "第二次变更日期",
        "THIRD_CHANGE_DATE": "第三次变更日期",
        "ACTUAL_PUBLISH_DATE": "实际发布日期",
        "SECURITY_TYPE_CODE": "证券类型代码",
        "SECURITY_TYPE": "证券类型",
        "TRADE_MARKET_CODE": "交易市场代码",
        "TRADE_MARKET": "交易市场",
        "REPORT_DATE": "报告日期",
        "APPOINT_PUBLISH_DATE": "任命发布日期",
        "RESIDUAL_DAYS": "剩余天数",
        "REPORT_TYPE_NAME": "报告类型名称",
        "IS_PUBLISH": "是否发布",
        "MARKET": "市场",
        "EITIME": "导入时间",
        "SECUCODE": "证券代码"
    }


class ScheduledDisclosure(APIDataV1RequestData):
    """查询 上市公司预约披露时间"""
    def __init__(
            self,
            security_code: Optional[str] = None,
            size: Optional[int] = 50,
            start_date: Optional[str] = None,
            end_date: Optional[str] = None,
            date: Optional[str] = None,
            industry_name: Optional[str] = None,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        """
        Notes:
            ```python
            from wisecon.stock.financial import ScheduledDisclosure

            data = ScheduledDisclosure(date="2024-09-30", size=5).load()
            data.to_frame(chinese_column=True)
            ```

        Args:
            security_code: 证券代码
            industry_name: 行业名称
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
        self.industry_name = industry_name
        self.mapping = ScheduledDisclosureMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs
        self.request_set(response_type="json", description="上市公司预约披露时间")
        self.conditions = []

    def params_filter(self) -> str:
        """
        :return:
        """
        self.filter_report_date()
        self.filter_security_code()
        return "".join(self.conditions)

    def params(self) -> Dict:
        """
        :return:
        """
        params = {
            "filter": self.params_filter(),
            "sortColumns": "FIRST_APPOINT_DATE,SECURITY_CODE",
            "sortTypes": "1,1",
            "pageSize": self.size,
            "pageNumber": 1,
            "reportName": "RPT_PUBLIC_BS_APPOIN",
        }
        return self.base_param(params)
