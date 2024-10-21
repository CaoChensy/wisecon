import json
from typing import Any, List, Dict, Callable, Optional
from wisecon.types import BaseRequestData, BaseMapping
from wisecon.utils import filter_str_by_mark


__all__ = [
    "FundValueMapping",
    "FundValue",
]


class FundValueMapping(BaseMapping):
    """"""
    columns: Dict = {
        "fundcode": "基金代码",
        "name": "基金名称",
        "jzrqv": "上一交易日",
        "dwjz": "基金净值（截止上一交易日）",
        "gsz": "估算净值（实时）",
        "gszzl": "估算涨幅（实时）",
        "gztime": "更新时间（实时）",
    }


class FundValue(BaseRequestData):
    """ Fund Value """
    def __init__(
            self,
            fund_code: str,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        """"""
        self.fund_code = fund_code
        self.mapping = FundValueMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs

        self.request_set(
            response_type="text",
            description="基金当前净值",
        )

    def base_url(self, ) -> str:
        """"""
        base_url = f"http://fundgz.1234567.com.cn/js/{self.fund_code}.js"
        return base_url

    def clean_content(
            self,
            content: Optional[str] = None,
    ) -> List[Dict]:
        """"""
        content = filter_str_by_mark(content)
        data = [json.loads(content)]
        return data