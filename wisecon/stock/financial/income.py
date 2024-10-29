from typing import Any, Dict, Literal, Callable, Optional
from wisecon.types import BaseMapping, APIDataV1RequestData


__all__ = [
    "StockIncome",
    "StockIncomeMapping",
]


TypeMarket = Literal["沪深A股", "沪市A股", "科创板", "深市A股", "创业板", "京市A股"]


class StockIncomeMapping(BaseMapping):
    """字段映射 上市公司利润报表"""
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
        "PARENT_NETPROFIT": "净利润",
        "TOTAL_OPERATE_INCOME": "营业总收入",
        "TOTAL_OPERATE_COST": "营业总支出",
        "TOE_RATIO": "营业利润率",
        "OPERATE_COST": "营业支出",
        "OPERATE_EXPENSE": "营业费用",
        "OPERATE_EXPENSE_RATIO": "营业费用占比",
        "SALE_EXPENSE": "销售费用",
        "MANAGE_EXPENSE": "管理费用",
        "FINANCE_EXPENSE": "财务费用",
        "OPERATE_PROFIT": "营业利润",
        "TOTAL_PROFIT": "总利润",
        "INCOME_TAX": "所得税",
        "OPERATE_INCOME": "营业收入",
        "INTEREST_NI": "利息净收入",
        "INTEREST_NI_RATIO": "利息净收入占比",
        "FEE_COMMISSION_NI": "手续费及佣金净收入",
        "FCN_RATIO": "手续费及佣金净收入占比",
        "OPERATE_TAX_ADD": "营业税金及附加",
        "MANAGE_EXPENSE_BANK": "银行管理费用",
        "FCN_CALCULATE": "手续费及佣金净收入计算",
        "INTEREST_NI_CALCULATE": "利息净收入计算",
        "EARNED_PREMIUM": "已赚保费",
        "EARNED_PREMIUM_RATIO": "已赚保费占比",
        "INVEST_INCOME": "投资收益",
        "SURRENDER_VALUE": "退保价值",
        "COMPENSATE_EXPENSE": "赔偿费用",
        "TOI_RATIO": "营业总收入同比",
        "OPERATE_PROFIT_RATIO": "营业利润率",
        "PARENT_NETPROFIT_RATIO": "净利润率",
        "DEDUCT_PARENT_NETPROFIT": "扣除后归属于母公司的净利润",
        "DPN_RATIO": "扣除后净利润率"
    }


class StockIncome(APIDataV1RequestData):
    """查询 上市公司利润报表"""
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
            from wisecon.stock.financial import StockIncome

            data = StockIncome(date="2024-09-30", size=5).load()
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
        self.mapping = StockIncomeMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs
        self.request_set(response_type="json", description="上市公司利润报表")
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
            "reportName": "RPT_DMSK_FN_INCOME",
        }
        return self.base_param(params)
