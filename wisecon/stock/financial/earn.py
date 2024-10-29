from typing import Any, Dict, Literal, Callable, Optional
from wisecon.types import BaseMapping, APIDataV1RequestData


__all__ = [
    "Earn",
    "EarnMapping",
]


class EarnMapping(BaseMapping):
    """字段映射 上市公司业绩报表"""
    columns: Dict = {
        "SECURITY_CODE": "证券代码",
        "SECURITY_NAME_ABBR": "证券简称",
        "TRADE_MARKET_CODE": "交易市场代码",
        "TRADE_MARKET": "交易市场",
        "SECURITY_TYPE_CODE": "证券类型代码",
        "SECURITY_TYPE": "证券类型",
        "UPDATE_DATE": "更新时间",
        "REPORTDATE": "报告日期",
        "BASIC_EPS": "每股收益(元)",
        "DEDUCT_BASIC_EPS": "扣除后基本每股收益",
        "TOTAL_OPERATE_INCOME": "营业总收入",
        "PARENT_NETPROFIT": "净利润",
        "WEIGHTAVG_ROE": "净资产收益率",
        "YSTZ": "营业收入同比增长(%)",
        "SJLTZ": "净利润同比增长(%)",
        "BPS": "每股净资产(元)",
        "MGJYXJJE": "每股经营现金流量(元)",
        "XSMLL": "销售毛利率",
        "YSHZ": "营业收入季度环比增长率(%)",
        "SJLHZ": "净利润季度环比增长率(%)",
        "ASSIGNDSCRPT": "分配说明",
        "PAYYEAR": "支付年份",
        "PUBLISHNAME": "行业",
        "ZXGXL": "资产结构",
        "NOTICE_DATE": "公告日期",
        "ORG_CODE": "机构代码",
        "TRADE_MARKET_ZJG": "交易市场信息",
        "ISNEW": "是否最新",
        "QDATE": "季度日期",
        "DATATYPE": "数据类型",
        "DATAYEAR": "数据年份",
        "DATEMMDD": "数据日期",
        "EITIME": "导入时间",
        "SECUCODE": "证券代码"
    }


class Earn(APIDataV1RequestData):
    """查询 上市公司业绩报表"""
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
            from wisecon.stock.financial import Earn

            data = Earn(date="2024-09-30", size=5).load()
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
        self.mapping = EarnMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs
        self.request_set(response_type="json", description="上市公司业绩报表")
        self.conditions = []

    def params_filter(self) -> str:
        """
        :return: 
        """
        if self.start_date:
            self.conditions.append(f"(REPORTDATE>='{self.start_date}')")
        if self.end_date:
            self.conditions.append(f"(REPORTDATE<='{self.end_date}')")
        if self.date:
            self.conditions.append(f"(REPORTDATE='{self.date}')")

        if self.security_code:
            self.conditions.append(f'(SECURITY_CODE="{self.security_code}")')

        if self.industry_name:
            self.conditions.append(f'(PUBLISHNAME="{self.industry_name}")')

        return "".join(self.conditions)

    def params(self) -> Dict:
        """
        :return:
        """
        params = {
            "filter": self.params_filter(),
            "sortColumns": "UPDATE_DATE,SECURITY_CODE",
            "sortTypes": "-1,-1",
            "pageSize": self.size,
            "pageNumber": 1,
            "reportName": "RPT_LICO_FN_CPD",
        }
        return self.base_param(params)
