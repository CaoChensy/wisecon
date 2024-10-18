from typing import Any, List, Dict, Callable, Optional
from wisecon.types import BaseMapping
from .base import MacroRequestData


__all__ = [
    "HoseIndexOldMapping",
    "HoseIndexOld",
    "HoseIndexNewMapping",
    "HoseIndexNew",
]


class HoseIndexOldMapping(BaseMapping):
    """"""
    columns: Dict = {
        "REPORT_DATE": "报告日期",
        "TIME": "时间",
        "HOSE_INDEX": "国房景气指数（指数值）",
        "HOSE_INDEX_SAME": "国房景气指数（同比增长）",
        "LAND_INDEX": "土地开发面积指数（指数值）",
        "LAND_INDEX_SAME": "土地开发面积指数（指数值）",
        "GOODSHOSE_INDEX": "销售价格指数（同比增长）",
        "GOODSHOSE_INDEX_SAME": "销售价格指数（同比增长）",
    }


class HoseIndexOld(MacroRequestData):
    """"""
    def __init__(
            self,
            size: Optional[int] = 20,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        self.size = size
        self.mapping = HoseIndexOldMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs
        self.request_set(description="中国 房价指数(08—10年)")

    def params(self) -> Dict:
        """
        :return:
        """
        columns = [
            "REPORT_DATE", "TIME", "HOSE_INDEX", "HOSE_INDEX_SAME", "LAND_INDEX",
            "LAND_INDEX_SAME", "GOODSHOSE_INDEX", "GOODSHOSE_INDEX_SAME"
        ]
        params = {
            "columns": ",".join(columns),
            "pageSize": self.size,
            "sortColumns": "REPORT_DATE",
            "sortTypes": "-1",
            "reportName": "RPT_ECONOMY_HOSE_INDEX",
        }
        return self.base_param(update=params)


class HoseIndexNewMapping(BaseMapping):
    """"""
    columns: Dict = {
        "REPORT_DATE": "时间",
        "CITY": "城市",
        "FIRST_COMHOUSE_SAME": "新建商品住宅价格指数（同比）",
        "FIRST_COMHOUSE_SEQUENTIAL": "新建商品住宅价格指数（环比）",
        "FIRST_COMHOUSE_BASE": "新建商品住宅价格指数（定基）",
        "SECOND_HOUSE_SAME": "二手住宅价格指数（同比）",
        "SECOND_HOUSE_SEQUENTIAL": "二手住宅价格指数（环比）",
        "SECOND_HOUSE_BASE": "二手住宅价格指数（定基）",
        "REPORT_DAY": "日期",
    }


class HoseIndexNew(MacroRequestData):
    """"""
    def __init__(
            self,
            cities: Optional[List[str]] = ["北京", "上海"],
            report_date: Optional[str] = None,
            size: Optional[int] = 20,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        """

        :param query_config:
        :param cities: 城市
        :param size: 数据量
        :param report_date: 日期
        :param verbose:
        :param logger:
        :param kwargs:
        """
        self.cities = cities
        self.report_date = report_date
        self.size = size
        self.mapping = HoseIndexNewMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs
        self.request_set(description="中国 新房价指数")

    def _data_filter(self):
        """"""
        if self.report_date:
            _filter = f"(REPORT_DATE='{self.report_date}')"
        elif self.cities:
            cities = [f'"{item}"' for item in self.cities]
            _filter = f'(CITY+in+({",".join(cities)}))'
        else:
            raise ValueError("report_date or cities must be set")
        return _filter

    def params(self) -> Dict:
        """
        :return:
        """
        columns = [
            "REPORT_DATE", "CITY", "FIRST_COMHOUSE_SAME", "FIRST_COMHOUSE_SEQUENTIAL",
            "FIRST_COMHOUSE_BASE", "SECOND_HOUSE_SAME", "SECOND_HOUSE_SEQUENTIAL",
            "SECOND_HOUSE_BASE", "REPORT_DAY"
        ]

        params = {
            "columns": ",".join(columns),
            "filter": self._data_filter(),
            "pageSize": self.size,
            "sortColumns": "REPORT_DATE,CITY",
            "sortTypes": "-1,-1",
            "reportName": "RPT_ECONOMY_HOUSE_PRICE",
        }
        return params
