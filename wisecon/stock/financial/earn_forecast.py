from typing import Any, Dict, Literal, Callable, Optional
from wisecon.types import BaseMapping, APIDataV1RequestData


__all__ = [
    "EarnForcast",
    "EarnForcastMapping",
]


class EarnForcastMapping(BaseMapping):
    """字段映射 上市公司业绩预告"""
    columns: Dict = {
        "SECUCODE": "证券代码",
        "SECURITY_CODE": "证券代码",
        "SECURITY_NAME_ABBR": "证券简称",
        "ORG_CODE": "机构代码",
        "NOTICE_DATE": "公告日期",
        "REPORT_DATE": "报告日期",
        "PREDICT_FINANCE_CODE": "预测财务指标代码",
        "PREDICT_FINANCE": "预测财务指标",
        "PREDICT_AMT_LOWER": "预测金额下限",
        "PREDICT_AMT_UPPER": "预测金额上限",
        "ADD_AMP_LOWER": "增长幅度下限",
        "ADD_AMP_UPPER": "增长幅度上限",
        "PREDICT_CONTENT": "预测内容",
        "CHANGE_REASON_EXPLAIN": "变动原因说明",
        "PREDICT_TYPE": "预测类型",
        "PREYEAR_SAME_PERIOD": "去年同期金额",
        "TRADE_MARKET": "交易市场",
        "TRADE_MARKET_CODE": "交易市场代码",
        "SECURITY_TYPE": "证券类型",
        "SECURITY_TYPE_CODE": "证券类型代码",
        "INCREASE_JZ": "增加金额",
        "FORECAST_JZ": "预测金额",
        "FORECAST_STATE": "预测状态",
        "IS_LATEST": "是否最新",
        "PREDICT_RATIO_LOWER": "预测比率下限",
        "PREDICT_RATIO_UPPER": "预测比率上限",
        "PREDICT_HBMEAN": "预测均值"
    }
    predict_finance_mapping: Dict = {
        "归母净利润": "004",
        "扣非净利润": "005",
        "每股收益": "003",
        "营业总收入": "006"
    }


class EarnForcast(APIDataV1RequestData):
    """查询 上市公司业绩预告"""
    def __init__(
            self,
            security_code: Optional[str] = None,
            size: Optional[int] = 50,
            start_date: Optional[str] = None,
            end_date: Optional[str] = None,
            date: Optional[str] = None,
            forcast_state: Optional[Literal["reduction", "increase"]] = None,
            predict_finance: Optional[Literal["归母净利润", "扣非净利润", "每股收益", "营业总收入"]] = None,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        """
        Notes:
            ```python
            from wisecon.stock.financial import EarnForcast

            data = EarnForcast(date="2024-09-30", size=5).load()
            data.to_frame(chinese_column=True)
            ```

        Args:
            security_code: 证券代码
            size: 数据条数据
            start_date: 开始日期
            end_date: 结束日期
            date: 指定日期
            forcast_state: 预测状态 `["reduction", "increase"]`
            predict_finance: 预测指标 `["归母净利润", "扣非净利润", "每股收益", "营业总收入"]`
            verbose: 是否打印日志
            logger: 日志对象
            **kwargs: 其他参数
        """
        self.security_code = security_code
        self.size = size
        self.start_date = start_date
        self.end_date = end_date
        self.date = date
        self.forcast_state = forcast_state
        self.predict_finance = predict_finance
        self.mapping = EarnForcastMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs
        self.request_set(response_type="json", description="上市公司业绩预告")
        self.conditions = []

    def params_filter(self) -> str:
        """"""
        self.filter_report_date()
        self.filter_security_code()
        if self.forcast_state:
            self.conditions.append(f'(FORECAST_STATE="{self.forcast_state}")')
        if self.predict_finance:
            self.conditions.append(f'(PREDICT_FINANCE_CODE="{self.mapping.predict_finance_mapping[self.predict_finance]}")')
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
            "reportName": "RPT_PUBLIC_OP_NEWPREDICT",
        }
        return self.base_param(params)
