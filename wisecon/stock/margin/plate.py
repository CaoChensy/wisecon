from typing import Any, Dict, Callable, Optional, Literal
from wisecon.types import BaseMapping, APIDataV1RequestData


__all__ = [
    "MarginTradingPlateMapping",
    "MarginTradingPlate",
]


class MarginTradingPlateMapping(BaseMapping):
    """字段映射 融资融券账户统计-板块融资融券"""
    columns: Dict = {
        "BOARD_CODE": "板块代码",
        "BOARD_NAME": "板块名称",
        "BOARD_TYPE": "板块类型",
        "BOARD_TYPE_CODE": "板块类型代码",
        "END_DATE": "结束日期",
        "FIN_BALANCE": "融资余额",
        "MARGIN_BALANCE": "保证金余额",
        "FIN_BALANCE_DIFF": "融资余额差额",
        "LOAN_NETSELL_AMT": "借入净卖出金额",
        "LOAN_BALANCE": "借入余额",
        "NOTLIMITED_MARKETCAP_A": "非限制市场总值A",
        "FIN_BALANCE_RATIO": "融资余额比例",
        "INTERVAL_TYPE": "区间类型",
        "FIN_BUY_AMT": "融资买入金额",
        "FIN_REPAY_AMT": "融资偿还金额",
        "LOAN_BALANCE_VOL": "借入余额量",
        "FIN_NETSELL_AMT": "融资净卖出金额",
        "LOAN_SELL_VOL": "借入卖出量",
        "LOAN_REPAY_VOL": "借入偿还量",
        "LOAN_SELL_AMT": "借入卖出金额",
        "FIN_NETBUY_AMT": "融资净买入金额"
    }


class MarginTradingPlate(APIDataV1RequestData):
    """查询 融资融券账户统计-板块融资融券"""
    def __init__(
            self,
            plate_name: Literal["行业", "概念", "地域"] = "行业",
            cycle: Literal[1, 3, 5, 10] = 1,
            size: Optional[int] = 50,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        """
        Notes:
            ```python
            from wisecon.stock.margin import *

            # 查询 融资融券账户统计-板块融资融券
            data = MarginTradingPlate(plate_name="行业").load()
            data.to_frame(chinese_column=True)
            ```

        Args:
            plate_name: 板块类型: `["行业", "概念", "地域"]`
            cycle: 统计周期
            size: 返回数据量
            verbose: 是否打印日志
            logger: 自定义日志打印函数
            **kwargs: 其他参数
        """
        self.plate_name = plate_name
        self.cycle = cycle
        self.size = size
        self.mapping = MarginTradingPlateMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs
        self.request_set(description="融资融券账户统计-板块融资融券")
        self.conditions = []

    def params_report_name(self) -> str:
        """"""
        if self.cycle == 1:
            return "RPTA_WEB_BKJYMXN"
        else:
            return "RPTA_WEB_BKQJYMXN"

    def params_plate_code(self) -> str:
        """"""
        plate_mapping = {"行业": "005", "概念": "006", "地域": "004"}
        return plate_mapping[self.plate_name]

    def params_filter(self) -> str:
        """"""
        self.conditions.append(f'(BOARD_TYPE_CODE="{self.params_plate_code()}")')
        if self.cycle > 1:
            self.conditions.append(f'(INTERVAL_TYPE="{self.cycle}日")')
        return "".join(self.conditions)

    def params(self) -> Dict:
        """"""
        params = {
            "reportName": self.params_report_name(),
            "sortColumns": "FIN_NETBUY_AMT",
            "sortTypes": "-1",
            "pageSize": self.size,
            "stat": self.cycle,
            "filter": self.params_filter(),
            "pageNo": "1",
        }
        return self.base_param(update=params)
