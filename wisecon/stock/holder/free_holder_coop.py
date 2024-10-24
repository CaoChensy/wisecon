from typing import Any, Dict, Literal, Callable, Optional
from wisecon.types import BaseMapping
from .base import StockFormRequestData


__all__ = [
    "FreeHolderCoop",
    "FreeHolderCoopMapping",
]


class FreeHolderCoopMapping(BaseMapping):
    """"""
    columns: Dict = {
        "HOLDER_NEW": "新的股东",
        "HOLDER_NAME": "股东名称",
        "HOLDER_TYPE": "股东类型",
        "COOPERAT_HOLDER_NEW": "合作股东代码",
        "COOPERAT_HOLDER_NAME": "合作股东姓名",
        "COOPERAT_HOLDER_TYPE": "合作股东类型",
        "COOPERAT_NUM": "合作持股数",
        "COOPERAT_SECURITYDATE": "合作证券日期",
        "PINGJIE": "评介"
    }


class FreeHolderCoop(StockFormRequestData):
    """"""
    def __init__(
            self,
            holder_name: Optional[str] = None,
            holder_type: Optional[Literal["个人", "基金", "QFII", "社保", "券商", "信托"]] = None,
            size: Optional[int] = 50,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        """

        :param size:
        :param start_date: 2024-09-30
        :param end_date: 2024-09-30
        :param date: 2024-09-30
        :param verbose:
        :param logger:
        :param kwargs:
        """
        self.holder_name = holder_name
        self.holder_type = holder_type
        self.size = size
        self.mapping = FreeHolderCoopMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs
        self.request_set(response_type="json", description="十大流通股东 - 股东协同")
        self.conditions = []

    def params_filter(self) -> str:
        """"""
        if self.holder_type:
            self.conditions.append(f'(HOLDER_TYPE="{self.holder_type}")')
        if self.holder_name:
            self.conditions.append(f'(HOLDER_NAME+like+"%{self.holder_name}%")')
        return "".join(self.conditions)

    def params(self) -> Dict:
        """
        :return:
        """
        params = {
            "filter": self.params_filter(),
            "sortColumns": "COOPERAT_NUM,HOLDER_NEW,COOPERAT_HOLDER_NEW",
            "sortTypes": "-1,-1,-1",
            "pageSize": self.size,
            "pageNumber": 1,
            "reportName": "RPT_COOPFREEHOLDER",
        }
        return self.base_param(params)
