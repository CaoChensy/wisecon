from bs4 import BeautifulSoup
from typing import Any, List, Dict, Callable, Optional
from wisecon.types import BaseMapping, BaseRequestData


__all__ = [
    "FundBaseMapping",
    "FundBase",
]


class FundBaseMapping(BaseMapping):
    """字段映射 基金基本信息"""
    columns: Dict = {
        'FullName': '基金全称',
        'ShortName': '基金简称',
        'FundCode': '基金代码',
        'FundType': '基金类型',
        'IssueDate': '发行日期',
        'EstablishmentDate/Capital': '成立日期/规模',
        'AssetSize': '资产规模',
        'ShareSize': '份额规模',
        'FundManager': '基金管理人',
        'Custodian': '基金托管人',
        'FundManagerPerson': '基金经理人',
        'DividendsSinceEstablishment': '成立来分红',
        'ManagementFeeRate': '管理费率',
        'CustodianFeeRate': '托管费率',
        'SalesServiceFeeRate': '销售服务费率',
        'MaximumSubscriptionFeeRate': '最高认购费率',
        'MaximumPurchaseFeeRate': '最高申购费率',
        'MaximumRedemptionFeeRate': '最高赎回费率',
        'PerformanceBenchmark': '业绩比较基准',
        'TrackingIndex': '跟踪标的'
    }


class FundBase(BaseRequestData):
    """查询 基金基本信息"""
    def __init__(
            self,
            fund_code: str,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        """
        Notes:
            ```python
            from wisecon.fund.fund_value import FundValue

            data = FundValue(fund_code="000001").load()
            data.to_frame(chinese_column=True)
            ```

        Args:
            fund_code: 基金代码
            verbose: 是否打印日志
            logger: 自定义日志
            **kwargs: 其他参数
        """
        self.fund_code = fund_code
        self.mapping = FundBaseMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs
        self.request_set(response_type="text", description="基金基本信息",)

    def base_url(self) -> str:
        """"""
        base_url = f"https://fundf10.eastmoney.com/jbgk_{self.fund_code}.html"
        return base_url

    def clean_content(
            self,
            content: Optional[str] = None,
    ) -> List[Dict]:
        """
        :return:
        """
        soup = BeautifulSoup(content, "html.parser")
        table_info = soup.find_all('table', {'class': 'info w790'})[0]
        td = [item.text for item in table_info.find_all('td')]
        data = dict(zip(list(self.mapping.columns.keys()), td))
        return [data]
