from typing import Any, Dict, Literal, Callable, Optional
from wisecon.types import BaseMapping, APIDataV1RequestData


__all__ = [
    "StockBalance",
    "StockBalanceMapping",
]


TypeMarket = Literal["沪深A股", "沪市A股", "科创板", "深市A股", "创业板", "京市A股"]


class StockBalanceMapping(BaseMapping):
    """字段映射 上市公司资产负债报表"""
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
        "TOTAL_ASSETS": "总资产",
        "FIXED_ASSET": "固定资产",
        "MONETARYFUNDS": "货币资金",
        "MONETARYFUNDS_RATIO": "货币资金占比",
        "ACCOUNTS_RECE": "应收账款",
        "ACCOUNTS_RECE_RATIO": "应收账款占比",
        "INVENTORY": "存货",
        "INVENTORY_RATIO": "存货占比",
        "TOTAL_LIABILITIES": "总负债",
        "ACCOUNTS_PAYABLE": "应付账款",
        "ACCOUNTS_PAYABLE_RATIO": "应付账款占比",
        "ADVANCE_RECEIVABLES": "预收账款",
        "ADVANCE_RECEIVABLES_RATIO": "预收账款占比",
        "TOTAL_EQUITY": "总权益",
        "TOTAL_EQUITY_RATIO": "总权益占比",
        "TOTAL_ASSETS_RATIO": "总资产占比",
        "TOTAL_LIAB_RATIO": "总负债占比",
        "CURRENT_RATIO": "流动比率",
        "DEBT_ASSET_RATIO": "资产负债率",
        "CASH_DEPOSIT_PBC": "现金存款（央行）",
        "CDP_RATIO": "现金存款占比",
        "LOAN_ADVANCE": "贷款预支",
        "LOAN_ADVANCE_RATIO": "贷款预支占比",
        "AVAILABLE_SALE_FINASSET": "可供出售金融资产",
        "ASF_RATIO": "可供出售金融资产占比",
        "LOAN_PBC": "央行贷款",
        "LOAN_PBC_RATIO": "央行贷款占比",
        "ACCEPT_DEPOSIT": "接受存款",
        "ACCEPT_DEPOSIT_RATIO": "接受存款占比",
        "SELL_REPO_FINASSET": "出售回购金融资产",
        "SRF_RATIO": "出售回购金融资产占比",
        "SETTLE_EXCESS_RESERVE": "结算超额准备金",
        "SER_RATIO": "超额准备金占比",
        "BORROW_FUND": "借款资金",
        "BORROW_FUND_RATIO": "借款资金占比",
        "AGENT_TRADE_SECURITY": "代理交易证券",
        "ATS_RATIO": "代理交易证券占比",
        "PREMIUM_RECE": "应收保费",
        "PREMIUM_RECE_RATIO": "应收保费占比",
        "SHORT_LOAN": "短期借款",
        "SHORT_LOAN_RATIO": "短期借款占比",
        "ADVANCE_PREMIUM": "预收保费",
        "ADVANCE_PREMIUM_RATIO": "预收保费占比"
    }


class StockBalance(APIDataV1RequestData):
    """查询 上市公司资产负债报表"""
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
            from wisecon.stock.financial import StockBalance

            data = StockBalance(date="2024-09-30", size=5).load()
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
        self.mapping = StockBalanceMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs
        self.request_set(response_type="json", description="上市公司资产负债报表")

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
        conditions = ['(SECURITY_TYPE_CODE in ("058001001","058001008"))']
        if self.start_date:
            conditions.append(f"(REPORT_DATE>='{self.start_date}')")
        if self.end_date:
            conditions.append(f"(REPORT_DATE<='{self.end_date}')")
        if self.date:
            conditions.append(f"(REPORT_DATE='{self.date}')")
        if self.market:
            conditions.append(self.params_tread_market())
        if self.industry_name:
            conditions.append(f'(INDUSTRY_NAME="{self.industry_name}")')
        if self.security_code:
            conditions.append(f'(SECURITY_CODE="{self.security_code}")')
        return "".join(conditions)

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
            "reportName": "RPT_DMSK_FN_BALANCE",
        }
        return self.base_param(params)
