from typing import Any, Dict, Optional, Callable
from wisecon.types import BaseMapping, APIAskSecretary
from wisecon.utils import jquery_mock_callback


__all__ = [
    "AskSecretary",
]


class AskSecretaryMapping(BaseMapping):
    """"""
    columns: Dict = {
        "id": "问题ID",
        "securityShortName": "证券简称",
        "title": "问题标题",
        "content": "回复内容",
        "createTime": "提问时间",
        "responseTime": "回复时间",
        "type": "问题类型",
        "headCharacter": "提问者名称",
        "gubaId": "股吧ID",
        "url": "原文链接"
    }


class AskSecretary(APIAskSecretary):
    """"""
    def __init__(
            self,
            keyword: str,
            start_date: str,
            end_date: str,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        """

        Args:
            node_name:
            date: yyyy-MM-dd
            security_code:
            verbose:
            logger:
            **kwargs:
        """
        self.keyword = keyword
        self.start_date = start_date
        self.end_date = end_date
        self.mapping = AskSecretaryMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs
        self.request_set(response_type="json", description="问董秘")

    def params(self) -> Dict:
        """"""
        params = {
            "cb": jquery_mock_callback(),
            "param": {
                "uid": "",
                "keyword": self.keyword,
                "type": ["wenDongMiWeb"],
                "client": "web",
                "clientVersion": "9.8",
                "clientType": "web",
                "param": {
                    "wenDongMiWeb": {
                        "webSearchScope": 4,
                        "pageindex": 1,
                        "pagesize": 10,
                        "startTime": f"{self.start_date} 00:00:00",
                        "endTime": f"{self.end_date} 00:00:00",
                        "preTag": "",
                        "postTag": ""
                    }
                }
            }
        }
        return self.base_param(update=params)
