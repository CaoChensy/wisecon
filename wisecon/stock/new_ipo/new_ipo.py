from typing import Any, Dict, Optional, Callable, Literal
from wisecon.types import BaseMapping, APIDataV1RequestData


__all__ = [
    "NewIPOListMapping",
    "NewIPOList",
]


class NewIPOListMapping(BaseMapping):
    """字段映射 新股申购与中签查询"""
    columns: Dict = {
        "SECURITY_CODE": "证券代码",
        "SECURITY_NAME": "证券名称",
        "TRADE_MARKET_CODE": "交易市场代码",
        "APPLY_CODE": "申购代码",
        "TRADE_MARKET": "交易市场",
        "MARKET_TYPE": "市场类型",
        "ORG_TYPE": "组织类型",
        "ISSUE_NUM": "发行数量",
        "ONLINE_ISSUE_NUM": "网上发行数量",
        "OFFLINE_PLACING_NUM": "网下配售数量",
        "TOP_APPLY_MARKETCAP": "最高申购市值",
        "PREDICT_ONFUND_UPPER": "预测资金上限",
        "ONLINE_APPLY_UPPER": "网上申购上限",
        "PREDICT_ONAPPLY_UPPER": "预测申购上限",
        "ISSUE_PRICE": "发行价格",
        "LATELY_PRICE": "最新价格",
        "CLOSE_PRICE": "收盘价格",
        "APPLY_DATE": "申购日期",
        "BALLOT_NUM_DATE": "摇号次数日期",
        "BALLOT_PAY_DATE": "摇号缴款日期",
        "LISTING_DATE": "上市日期",
        "AFTER_ISSUE_PE": "发行后市盈率",
        "ONLINE_ISSUE_LWR": "网上发行下限",
        "INITIAL_MULTIPLE": "初始倍数",
        "INDUSTRY_PE_NEW": "行业新市盈率",
        "OFFLINE_EP_OBJECT": "网下配售对象",
        "CONTINUOUS_1WORD_NUM": "连续1字数",
        "TOTAL_CHANGE": "总变化",
        "PROFIT": "利润",
        "LIMIT_UP_PRICE": "涨停价格",
        "INFO_CODE": "信息代码",
        "OPEN_PRICE": "开盘价格",
        "LD_OPEN_PREMIUM": "开盘溢价",
        "LD_CLOSE_CHANGE": "收盘变动",
        "TURNOVERRATE": "换手率",
        "LD_HIGH_CHANG": "最高变化",
        "LD_AVERAGE_PRICE": "平均价格",
        "OPEN_DATE": "开盘日期",
        "OPEN_AVERAGE_PRICE": "开盘平均价格",
        "PREDICT_PE": "预测市盈率",
        "PREDICT_ISSUE_PRICE2": "预测发行价格2",
        "PREDICT_ISSUE_PRICE": "预测发行价格",
        "PREDICT_ISSUE_PRICE1": "预测发行价格1",
        "PREDICT_ISSUE_PE": "预测发行市盈率",
        "PREDICT_PE_THREE": "预测市盈率三",
        "ONLINE_APPLY_PRICE": "网上申购价格",
        "MAIN_BUSINESS": "主营业务",
        "PAGE_PREDICT_PRICE1": "页面预测价格1",
        "PAGE_PREDICT_PRICE2": "页面预测价格2",
        "PAGE_PREDICT_PRICE3": "页面预测价格3",
        "PAGE_PREDICT_PE1": "页面预测市盈率1",
        "PAGE_PREDICT_PE2": "页面预测市盈率2",
        "PAGE_PREDICT_PE3": "页面预测市盈率3",
        "SELECT_LISTING_DATE": "选择上市日期",
        "IS_BEIJING": "是否北京",
        "INDUSTRY_PE_RATIO": "行业市盈率",
        "INDUSTRY_PE": "行业市盈率",
        "IS_REGISTRATION": "是否注册",
        "IS_REGISTRATION_NEW": "是否新注册",
        "NEWEST_PRICE": "最新价格",

        # RPT_NEEQ_ISSUEINFO_LIST
        "ORG_CODE": "组织代码",
        "SECUCODE": "证券代码",
        "SECURITY_NAME_ABBR": "证券简称",
        "EXPECT_ISSUE_NUM": "预计发行数量",
        "PRICE_WAY": "定价方式",
        "ISSUE_PE_RATIO": "发行市盈率",
        "RESULT_NOTICE_DATE": "结果公告日期",
        "APPLY_AMT_UPPER": "申购金额上限",
        "APPLY_NUM_UPPER": "申购股数上限",
        "ONLINE_PAY_DATE": "网上缴款日期",
        "ONLINE_REFUND_DATE": "网上退款日期",
        "PER_SHARES_INCOME": "每股收益",
        "AMPLITUDE": "波动幅度",
        "ONLINE_APPLY_LOWER": "网上申购下限",
        "APPLY_AMT_100": "100股申购金额",
        "TAKE_UP_TIME": "占用时间",
        "CAPTURE_PROFIT": "捕获利润",
        "APPLY_SHARE_100": "100股申购股数",
        "AVERAGE_PRICE": "平均价格",
        "ORG_VAN": "组织价值",
        "VA_AMT": "价值金额",
        "ISSUE_PRICE_ADJFACTOR": "发行价格调整因子",
        "FRIST_CLOSE_CHANGE": "首日收盘变动",
        "f14": "备用字段1",
        "f2": "备用字段2",
        "f3": "备用字段3",
        "NEW_CHANGE_RATE": "新变动率",

        # RPT_BOND_CB_LIST
        "DELIST_DATE": "退市日期",
        "CONVERT_STOCK_CODE": "可转股票代码",
        "BOND_EXPIRE": "到期年限",
        "RATING": "评级",
        "VALUE_DATE": "价值日期",
        "ISSUE_YEAR": "发行年份",
        "CEASE_DATE": "停止交易日期",
        "EXPIRE_DATE": "到期日期",
        "PAY_INTEREST_DAY": "付息日",
        "INTEREST_RATE_EXPLAIN": "利率说明",
        "BOND_COMBINE_CODE": "债券组合代码",
        "ACTUAL_ISSUE_SCALE": "实际发行规模",
        "PAR_VALUE": "面值",
        "ISSUE_OBJECT": "发行对象",
        "REDEEM_TYPE": "赎回类型",
        "EXECUTE_REASON_HS": "执行原因HS",
        "NOTICE_DATE_HS": "通知日期HS",
        "NOTICE_DATE_SH": "通知日期SH",
        "EXECUTE_PRICE_HS": "执行价格HS",
        "EXECUTE_PRICE_SH": "执行价格SH",
        "RECORD_DATE_SH": "登记日期SH",
        "EXECUTE_START_DATESH": "执行开始日期SH",
        "EXECUTE_START_DATEHS": "执行开始日期HS",
        "EXECUTE_END_DATE": "执行结束日期",
        "CORRECODE": "更正代码",
        "CORRECODE_NAME_ABBR": "更正简称",
        "PUBLIC_START_DATE": "公开发行开始日期",
        "CORRECODEO": "更正代码O",
        "CORRECODE_NAME_ABBRO": "更正简称O",
        "BOND_START_DATE": "债券开始日期",
        "SECURITY_START_DATE": "证券开始日期",
        "SECURITY_SHORT_NAME": "证券简称",
        "FIRST_PER_PREPLACING": "首次转让预售",
        "ONLINE_GENERAL_AAU": "网上发行一般额度",
        "ONLINE_GENERAL_LWR": "网上发行下限",
        "INITIAL_TRANSFER_PRICE": "初始转让价格",
        "TRANSFER_END_DATE": "转让结束日期",
        "TRANSFER_START_DATE": "转让开始日期",
        "RESALE_CLAUSE": "转售条款",
        "REDEEM_CLAUSE": "赎回条款",
        "PARTY_NAME": "评级机构名称",
        "CONVERT_STOCK_PRICE": "可转股票价格",
        "TRANSFER_PRICE": "转让价格",
        "TRANSFER_VALUE": "转让价值",
        "CURRENT_BOND_PRICE": "当前债券价格",
        "TRANSFER_PREMIUM_RATIO": "转让溢价比率",
        "CONVERT_STOCK_PRICEHQ": "可转股票价格HQ",
        "MARKET": "市场",
        "RESALE_TRIG_PRICE": "转售触发价格",
        "REDEEM_TRIG_PRICE": "赎回触发价格",
        "PBV_RATIO": "市净率",
        "IB_START_DATE": "IB开始日期",
        "IB_END_DATE": "IB结束日期",
        "CASHFLOW_DATE": "现金流日期",
        "COUPON_IR": "票息利率",
        "PARAM_NAME": "发行参数名称",
        "ISSUE_TYPE": "发行类型",
        "EXECUTE_REASON_SH": "执行原因SH",
        "PAYDAYNEW": "新支付日",
        "CURRENT_BOND_PRICENEW": "当前债券价格新",
        "IS_CONVERT_STOCK": "是否可转股",
        "IS_REDEEM": "是否可赎回",
        "IS_SELLBACK": "是否可回售",
        "FIRST_PROFIT": "首次收益",
        # RPT_CUSTOM_REITS_APPLY_LIST_MARKET
        "SECURITY_INNER_CODE": "证券内部代码",
        "SALE_PRICE": "销售价格",
        "SUBSCRIBE_LOW_NUM": "最低申购金额",
        "ALLOW_SCALE": "允许规模",
        "RAISE_SHARE": "募集份额",
        "RINISTRRATIO": "认购比例",
        "VALID_SUBSCRIBE_MULTIPLE": "有效申购倍数",
        "SUBSCRIBE_START_DATE": "申购开始日期",
        "PUBLIC_VSA_RATIO": "公开发行比例",
        "SUBSCRIBE_END_DATE": "申购结束日期",
        "LTD_SECURITY_NAME": "有限责任公司证券名称",
        "PUBLIC_SHARE": "公开发行股份",
        "SUBSCRIBE_DATE": "申购日期",
        "ENQUIRY_DATE": "询价日期",
        "QUOTA_NONUNIT": "非单位配额",
        "IS_APPLYING": "是否正在申购",
        "IS_LISTING_SHOW": "是否显示上市",
        "PUBLIC_VS_SHARE": "公开发行对比股份",
        "OFFLINE_VS_SHARE": "线下发行对比股份",
        "PUBLIC_VS_MULTIPLE": "公开发行倍数",
        "OFFLINE_VS_MULTIPLE": "线下发行倍数",
        "LD_CHANGE_RATE": "最新变动率",
        "EXPAND_NAME_ABBR": "扩展名称简称",
        "OFFLINE_VSA_RATIO": "线下发行比例",
        "ITEM_TYPE": "项目类型",
        "ITEMTYPE_NAME": "项目类型名称",
        "START_DATE": "开始日期",
        "END_DATE": "结束日期",
        "OPEN": "开盘",
        "CHG": "变动",
        "DTNAVDATE": "日期净值",
        "DTANVPER": "净值周期",
        "DIVIDEND_RATE_TTM": "股息率（TTM）",
        "OPEN_YIELD": "开盘收益",
        "SALE_PRICE_CHG": "销售价格变动",
        "J_PRICE_CHG": "价格变动",
        "PREDICT_RAISE_SCALE": "预测募集规模",
        "NEED_FUND": "所需资金",
        "LD_YIELD": "最新收益",
        "WEEK_START_DATE": "周开始日期",
        "DIVIDEND_RATIO": "股息比率",
        "NEW_DISCOUNT_RATIO": "新折扣率",
        "NEW_DIVIDEND_RATE_TTM": "新股息率（TTM）",
    }


class NewIPOList(APIDataV1RequestData):
    """查询 新股申购与中签查询"""
    def __init__(
            self,
            market: Optional[Literal["全部股票", "沪市主板", "科创板", "深市主板", "创业板", "北交所", "可转债", "REITs"]] = "全部股票",
            size: Optional[int] = 50,
            start_date: Optional[str] = "2010-01-01",
            end_date: Optional[str] = None,
            date: Optional[str] = None,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        """
        Notes:
            ```python
            from wisecon.stock.new_ipo import *

            data = NewIPOList(market="全部股票").load()
            data.to_frame(chinese_column=True)

            data = NewIPOList(market="沪市主板").load()
            data.to_frame(chinese_column=True)

            data = NewIPOList(market="科创板").load()
            data.to_frame(chinese_column=True)

            data = NewIPOList(market="深市主板").load()
            data.to_frame(chinese_column=True)

            data = NewIPOList(market="创业板").load()
            data.to_frame(chinese_column=True)

            data = NewIPOList(market="北交所").load()
            data.to_frame(chinese_column=True)

            data = NewIPOList(market="可转债").load()
            data.to_frame(chinese_column=True)

            data = NewIPOList(market="REITs").load()
            data.to_frame(chinese_column=True)
            ```

        Args:
            market: 股票市场，默认为全部股票， ["沪市主板", "科创板", "深市主板", "创业板", "北交所", "可转债", "REITs"]
            size: 返回数据条数
            start_date: 开始日期
            end_date: 结束日期
            date: 指定日期
            verbose: 是否显示详细信息
            logger: 日志记录器
            **kwargs: 其他参数
        """
        self.market = market
        self.size = size
        self.start_date = start_date
        self.end_date = end_date
        self.date = date
        self.mapping = NewIPOListMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs
        self.request_set(description="新股申购与中签查询")
        self.conditions = []
        self.validate_date_format(date=[start_date, end_date, date])

    def params_tread_market(self):
        """"""
        market_mapping = {
            "沪市主板": "(SECURITY_TYPE_CODE in (\"058001001\",\"058001008\"))(TRADE_MARKET_CST=\"0101\")",
            "科创板": "(SECURITY_TYPE_CODE in (\"058001001\",\"058001008\"))(TRADE_MARKET_CST=\"0102\")",
            "深市主板": "(SECURITY_TYPE_CODE=\"058001001\")(TRADE_MARKET_CST=\"0201\")",
            "创业板": "(SECURITY_TYPE_CODE=\"058001001\")(TRADE_MARKET_CST=\"0202\")",
        }
        if self.market in market_mapping:
            self.conditions.append(market_mapping[self.market])

    def params_update(self) -> Dict:
        """"""
        if self.market in ["全部股票", "沪市主板", "科创板", "深市主板", "创业板"]:
            return dict()
        elif self.market == "北交所":
            return {
                "columns": "ALL",
                "sortColumns": "APPLY_DATE",
                "sortTypes": "-1",
                "reportName": "RPT_NEEQ_ISSUEINFO_LIST",
                "quoteColumns": "f14,f2~01~SECURITY_CODE,f3~01~SECURITY_CODE,NEW_CHANGE_RATE~01~SECURITY_CODE",
                "quoteType": "0",
                "source": "NEEQSELECT",
            }
        elif self.market == "可转债":
            return {
                "sortColumns": "PUBLIC_START_DATE,SECURITY_CODE",
                "sortTypes": "-1,-1",
                "reportName": "RPT_BOND_CB_LIST",
                "columns": "ALL",
                "quoteColumns": "f2~01~CONVERT_STOCK_CODE~CONVERT_STOCK_PRICE,f235~10~SECURITY_CODE~TRANSFER_PRICE,f236~10~SECURITY_CODE~TRANSFER_VALUE,f2~10~SECURITY_CODE~CURRENT_BOND_PRICE,f237~10~SECURITY_CODE~TRANSFER_PREMIUM_RATIO,f239~10~SECURITY_CODE~RESALE_TRIG_PRICE,f240~10~SECURITY_CODE~REDEEM_TRIG_PRICE,f23~01~CONVERT_STOCK_CODE~PBV_RATIO",
                "quoteType": "0",
            }
        elif self.market == "REITs":
            return {
                "sortColumns": "SUBSCRIBE_START_DATE",
                "sortTypes": "-1",
                "reportName": "RPT_CUSTOM_REITS_APPLY_LIST_MARKET",
                "columns": "ALL",
                "quoteColumns": "f14~09~SECURITY_CODE~LTD_SECURITY_NAME,f2~09~SECURITY_CODE~f2,NEW_DISCOUNT_RATIO~09~SECURITY_CODE,NEW_CHANGE_RATE~09~SECURITY_CODE,NEW_DIVIDEND_RATE_TTM~09~SECURITY_CODE",
            }
        else:
            raise ValueError(f"market: {self.market} is not valid.")

    def params_filter(self) -> str:
        """"""
        if self.market not in ["可转债", "REITs"]:
            self.filter_report_date(date_name="APPLY_DATE")
        self.params_tread_market()
        return "".join(self.conditions)

    def params(self) -> Dict:
        """"""
        columns = [
            "SECURITY_CODE", "SECURITY_NAME", "TRADE_MARKET_CODE", "APPLY_CODE", "TRADE_MARKET",
            "MARKET_TYPE", "ORG_TYPE", "ISSUE_NUM", "ONLINE_ISSUE_NUM", "OFFLINE_PLACING_NUM",
            "TOP_APPLY_MARKETCAP", "PREDICT_ONFUND_UPPER", "ONLINE_APPLY_UPPER", "PREDICT_ONAPPLY_UPPER",
            "ISSUE_PRICE", "LATELY_PRICE", "CLOSE_PRICE", "APPLY_DATE", "BALLOT_NUM_DATE",
            "BALLOT_PAY_DATE", "LISTING_DATE", "AFTER_ISSUE_PE", "ONLINE_ISSUE_LWR", "INITIAL_MULTIPLE",
            "INDUSTRY_PE_NEW", "OFFLINE_EP_OBJECT", "CONTINUOUS_1WORD_NUM", "TOTAL_CHANGE", "PROFIT",
            "LIMIT_UP_PRICE", "INFO_CODE", "OPEN_PRICE", "LD_OPEN_PREMIUM", "LD_CLOSE_CHANGE",
            "TURNOVERRATE", "LD_HIGH_CHANG", "LD_AVERAGE_PRICE", "OPEN_DATE", "OPEN_AVERAGE_PRICE",
            "PREDICT_PE", "PREDICT_ISSUE_PRICE2", "PREDICT_ISSUE_PRICE", "PREDICT_ISSUE_PRICE1",
            "PREDICT_ISSUE_PE", "PREDICT_PE_THREE", "ONLINE_APPLY_PRICE", "MAIN_BUSINESS",
            "PAGE_PREDICT_PRICE1", "PAGE_PREDICT_PRICE2", "PAGE_PREDICT_PRICE3", "PAGE_PREDICT_PE1",
            "PAGE_PREDICT_PE2", "PAGE_PREDICT_PE3", "SELECT_LISTING_DATE", "IS_BEIJING", "INDUSTRY_PE_RATIO",
            "INDUSTRY_PE", "IS_REGISTRATION",
        ]
        params = {
            "sortColumns": "APPLY_DATE,SECURITY_CODE",
            "sortTypes": "-1,-1",
            "pageSize": self.size,
            "reportName": "RPTA_APP_IPOAPPLY",
            "columns": ",".join(columns),
            "quoteColumns": "f2~01~SECURITY_CODE~NEWEST_PRICE",
            "quoteType": "0",
            "filter": self.params_filter(),
        }
        params.update(self.params_update())
        return self.base_param(update=params)
