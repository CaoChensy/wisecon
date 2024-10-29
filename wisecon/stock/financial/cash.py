from typing import Any, Dict, Literal, Callable, Optional
from wisecon.types import BaseMapping, APIDataV1RequestData


__all__ = [
    "StockCashFlow",
    "StockCashFlowMapping",
]


TypeMarket = Literal["沪深A股", "沪市A股", "科创板", "深市A股", "创业板", "京市A股"]


class StockCashFlowMapping(BaseMapping):
    """字段映射 上市公司现金流量报表"""
    columns: Dict = {
        "SECUCODE": "证券代码",
        "SECURITY_CODE": "证券代码",
        "INDUSTRY_CODE": "行业代码",
        "ORG_CODE": "机构代码",
        "SECURITY_NAME_ABBR": "证券简称",
        "INDUSTRY_NAME": "行业名称",
        "MARKET": "市场",
        "SECURITY_TYPE_CODE": "证券类型代码",
        "TRADE_MARKET_CODE": "交易市场代码",
        "DATE_TYPE_CODE": "日期类型代码",
        "REPORT_TYPE_CODE": "报告类型代码",
        "DATA_STATE": "数据状态",
        "NOTICE_DATE": "公告日期",
        "REPORT_DATE": "报告日期",
        "NETCASH_OPERATE": "经营活动净现金流量",
        "NETCASH_OPERATE_RATIO": "经营活动净现金流量占比",
        "SALES_SERVICES": "销售服务收入",
        "SALES_SERVICES_RATIO": "销售服务收入占比",
        "PAY_STAFF_CASH": "支付员工现金",
        "PSC_RATIO": "支付员工现金占比",
        "NETCASH_INVEST": "投资活动净现金流量",
        "NETCASH_INVEST_RATIO": "投资活动净现金流量占比",
        "RECEIVE_INVEST_INCOME": "收到投资收益",
        "RII_RATIO": "收到投资收益占比",
        "CONSTRUCT_LONG_ASSET": "长期资产建设",
        "CLA_RATIO": "长期资产建设占比",
        "NETCASH_FINANCE": "融资活动净现金流量",
        "NETCASH_FINANCE_RATIO": "融资活动净现金流量占比",
        "CCE_ADD": "现金及现金等价物增加额",
        "CCE_ADD_RATIO": "现金及现金等价物增加额占比",
        "CUSTOMER_DEPOSIT_ADD": "客户存款增加额",
        "CDA_RATIO": "客户存款增加额占比",
        "DEPOSIT_IOFI_OTHER": "其他存款",
        "DIO_RATIO": "其他存款占比",
        "LOAN_ADVANCE_ADD": "贷款预支增加额",
        "LAA_RATIO": "贷款预支增加额占比",
        "RECEIVE_INTEREST_COMMISSION": "收到利息及佣金",
        "RIC_RATIO": "收到利息及佣金占比",
        "INVEST_PAY_CASH": "投资支付现金",
        "IPC_RATIO": "投资支付现金占比",
        "BEGIN_CCE": "期初现金及现金等价物",
        "BEGIN_CCE_RATIO": "期初现金及现金等价物占比",
        "END_CCE": "期末现金及现金等价物",
        "END_CCE_RATIO": "期末现金及现金等价物占比",
        "RECEIVE_ORIGIC_PREMIUM": "收到原保险保费",
        "ROP_RATIO": "收到原保险保费占比",
        "PAY_ORIGIC_COMPENSATE": "支付原保险赔偿",
        "POC_RATIO": "支付原保险赔偿占比"
    }


class StockCashFlow(APIDataV1RequestData):
    """查询 上市公司现金流量报表"""
    def __init__(
            self,
            security_code: Optional[str] = None,
            market: Optional[TypeMarket] = None,
            industry_name: Optional[str] = None,
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
            from wisecon.stock.financial import StockCashFlow

            data = StockCashFlow(date="2024-09-30", size=5).load()
            data.to_frame(chinese_column=True)
            ```

        Args:
            security_code: 证券代码
            market: 市场: `["沪深A股", "沪市A股", "科创板", "深市A股", "创业板", "京市A股"]`
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
        self.market = market
        self.industry_name = industry_name
        self.size = size
        self.start_date = start_date
        self.end_date = end_date
        self.date = date
        self.mapping = StockCashFlowMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs
        self.request_set(response_type="json", description="上市公司现金流量报表")
        self.conditions = []

    def params_tread_market(self) -> str:
        """"""
        market_mapping = {
            "沪深A股": 'TRADE_MARKET_CODE!="069001017")',
            "沪市A股": 'TRADE_MARKET_CODE+in+("069001001001","069001001003","069001001006"))',
            "科创板": '(TRADE_MARKET_CODE="069001001006")',
            "深市A股": 'TRADE_MARKET_CODE+in+("069001002001","069001002002","069001002003","069001002005"))',
            "创业板": '(TRADE_MARKET_CODE="069001002002")',
            "京市A股": 'TRADE_MARKET_CODE="069001017")',
        }
        return market_mapping[self.market]

    def params_filter(self) -> str:
        """"""
        self.conditions.append('(SECURITY_TYPE_CODE in ("058001001","058001008"))')
        self.filter_report_date()
        self.filter_security_code()
        if self.market:
            self.conditions.append(self.params_tread_market())
        if self.industry_name:
            self.conditions.append(f'(INDUSTRY_NAME="{self.industry_name}")')
        return "".join(self.conditions)

    def params(self) -> Dict:
        """
        :return:
        """
        params = {
            "filter": self.params_filter(),
            "sortColumns": "NOTICE_DATE,SECURITY_CODE",
            "sortTypes": "-1,-1",
            "pageSize": self.size,
            "pageNumber": 1,
            "reportName": "RPT_DMSK_FN_CASHFLOW",
        }
        return self.base_param(params)
