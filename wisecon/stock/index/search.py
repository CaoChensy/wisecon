from wisecon.types import APISearch, BaseMapping
from typing import Any, Dict, Callable, Optional


__all__ = [
    "SearchKeyword",
    "SearchMapping",
]


class SearchMapping(BaseMapping):
    """ 搜索映射类 """
    columns: Dict = {
        "code": "板块代码",
        "innerCode": "内部代码",
        "shortName": "板块简称",
        "market": "市场代码",
        "pinyin": "拼音缩写",
        "securityType": "证券类型编码",
        "securityTypeName": "证券类型名称",
        "smallType": "小类代码",
        "status": "状态",
        "flag": "标志位",
        "extSmallType": "扩展小类代码"
    }


class SearchKeyword(APISearch):
    """ 搜索关键词，查询板块、行业、概念、地域、指数、基金、股票等信息 """
    def __init__(
            self,
            keyword: str = None,
            size: Optional[int] = 5,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        """
        Notes:
            ```python
            from wisecon.stock.index import *

            data = SearchKeyword(keyword="新能源").load()
            data.to_frame(chinese_column=True)
            ```

        Args:
            keyword: 搜索关键词
            size: 返回条数
            verbose: 是否打印日志
            logger: 自定义日志
            **kwargs: 其他参数
        """
        self.keyword = keyword
        self.size = size
        self.mapping = SearchMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs
        self.request_set(response_type="json", description="搜索关键词，查询板块、行业、概念、地域、指数、基金、股票等信息")
        self.conditions = []

    def params(self) -> Dict:
        """
        :return:
        """
        params = {
            "keyword": self.keyword,
            "pageSize": self.size,
        }
        return self.base_param(params)
