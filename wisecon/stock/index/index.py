from typing import Any, Dict, Literal, Callable, Optional
from wisecon.types import BaseMapping, APIDataV1RequestData


__all__ = [
    "IndexStock",
    "IndexStockMapping",
]


class IndexStockMapping(BaseMapping):
    """字段映射 指数成分股数据"""
    columns: Dict = {
        "SECUCODE": "证券代码",
        "SECURITY_CODE": "证券代码",
        "TYPE": "类型",
        "SECURITY_NAME_ABBR": "证券简称",
        "CLOSE_PRICE": "收盘价",
        "INDUSTRY": "行业",
        "REGION": "地区",
        "WEIGHT": "权重",
        "EPS": "每股收益",
        "BPS": "每股净资产",
        "ROE": "净资产收益率",
        "TOTAL_SHARES": "总股份",
        "FREE_SHARES": "自由流通股份",
        "FREE_CAP": "自由流通市值",
        "f2": "最新价",
        "f3": "涨跌幅"
    }


class IndexStock(APIDataV1RequestData):
    """查询 指数成分股数据"""
    def __init__(
            self,
            index_name: Optional[Literal["沪深300", "上证50", "中证500", "科创50"]] = None,
            size: Optional[int] = 50,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        """
        Notes:
            ```python
            from wisecon.stock.index import *

            data = IndexStock(index_name="沪深300", size=5).load()
            data.to_frame(chinese_column=True)
            ```

        Args:
            index_name: 指数名称`["沪深300", "上证50", "中证500", "科创50"]`
            size: 返回条数
            verbose: 是否打印日志
            logger: 自定义日志
            **kwargs: 其他参数
        """
        self.index_name = index_name
        self.size = size
        self.mapping = IndexStockMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs
        self.request_set(response_type="json", description="指数成分股数据")
        self.conditions = []

    def params_index_name(self) -> str:
        """"""
        index_name_mapping = {"沪深300": "1", "上证50": "2", "中证500": "3", "科创50": "4"}
        if self.index_name:
            return index_name_mapping.get(self.index_name, "1")
        else:
            return "1"

    def params_filter(self) -> str:
        """"""
        self.conditions.append(f'(TYPE="{self.params_index_name()}")')
        return "".join(self.conditions)

    def params(self) -> Dict:
        """
        :return:
        """
        columns = [
            "SECUCODE", "SECURITY_CODE", "TYPE", "SECURITY_NAME_ABBR", "CLOSE_PRICE",
            "INDUSTRY", "REGION", "WEIGHT", "EPS", "BPS", "ROE", "TOTAL_SHARES",
            "FREE_SHARES", "FREE_CAP",
        ]

        params = {
            "columns": ",".join(columns),
            "quoteColumns": "f2,f3",
            "quoteType": "0",
            "filter": self.params_filter(),
            "sortColumns": "SECURITY_CODE",
            "sortTypes": "-1",
            "pageSize": self.size,
            "pageNumber": 1,
            "reportName": "RPT_INDEX_TS_COMPONENT",
        }
        return self.base_param(params)
