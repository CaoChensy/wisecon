import json
from typing import Any, List, Dict, Tuple, Callable, Optional
from wisecon.types import BaseMapping, BaseRequestData, ResponseData, Metadata


__all__ = [
    "FundCompanyMapping",
    "FundCompany",
]


class FundCompanyMapping(BaseMapping):
    """"""
    columns: Dict = {
        "company_code": "公司代码",
        "company_name": "公司名称",
    }


class FundCompany(BaseRequestData):
    """ Fund Company """
    def __init__(
            self,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        """"""
        self.mapping = FundCompanyMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs

        self.request_set(
            response_type="text",
            description="基金公司代码",
        )

    def base_url(self) -> str:
        """"""
        base_url = "http://fund.eastmoney.com/js/jjjz_gs.js"
        return base_url

    def clean_content(
            self,
            content: Optional[str],
    ) -> List[Dict]:
        """"""
        columns = list(self.mapping.columns.keys())
        content = content[content.find("["): content.rfind("]") + 1]
        data = json.loads(content)
        data = [dict(zip(columns, item)) for item in data]
        return data
