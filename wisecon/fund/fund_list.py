import json
from typing import Any, List, Dict, Callable, Optional
from wisecon.types import BaseMapping, BaseRequestData
from wisecon.utils import filter_str_by_mark


__all__ = [
    "FundListMapping",
    "FundList",
]


class FundListMapping(BaseMapping):
    """字段映射 全部基金列表"""
    columns: Dict = {
        "fund_code": "基金代码",
        "fund_pinyin": "基金拼音简写",
        "fund_name": "基金名称",
        "fund_type": "基金类型",
        "fund_pinyin_full": "基金拼音全称"
    }


class FundList(BaseRequestData):
    """查询 全部基金列表"""
    def __init__(
            self,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        """
        Notes:
            ```python
            from wisecon.fund import *

            data = FundList().load()
            data.to_frame(chinese_column=True)
            ```

        Args:
            verbose: 是否打印日志
            logger: 自定义日志
            **kwargs: 其他参数
        """
        self.mapping = FundListMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs
        self.request_set(
            response_type="text",
            description="基金列表",
        )

    def base_url(self) -> str:
        """"""
        base_url = "http://fund.eastmoney.com/js/fundcode_search.js"
        return base_url

    def clean_content(self, content: Optional[str]) -> List[Dict]:
        """"""
        content = filter_str_by_mark(s=content, start="[", end="]")
        data = json.loads(content)

        columns = list(self.mapping.columns.keys())

        def _clean_data(item):
            """"""
            return dict(zip(columns, item))

        data = list(map(_clean_data, data))
        return data
