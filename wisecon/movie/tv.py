from typing import Any, Dict, Callable, Literal, Optional, Annotated
from wisecon.types import BaseMapping
from wisecon.types.request_api.movie import APITVRequestData


__all__ = [
    "TVMapping",
    "TV",
]


class TVMapping(BaseMapping):
    """字段映射 实时电视收视率"""
    columns: Dict = {
        "attentionRate": "关注率",
        "attentionRateDesc": "关注率描述",
        "channelName": "频道名称",
        "marketRate": "市场份额",
        "marketRateDesc": "市场份额描述",
        "programmeName": "节目名称"
    }


class TV(APITVRequestData):
    """查询 实时电视收视率"""
    def __init__(
            self,
            source: Annotated[Literal["央视", "卫视"], "", True] = "央视",
            verbose: Annotated[Optional[bool], "", False] = False,
            logger: Annotated[Optional[Callable], "", False] = None,
            **kwargs: Annotated[Any, "", False],
    ):
        """
        Notes:
            ```python
            from wisecon.movie import *

            # 查询 央视实时电视收视率
            data = TV(source="央视").load()
            data.to_frame(chinese_column=True)

            # 查询 卫视实时电视收视率
            data = TV(source="卫视").load()
            data.to_frame(chinese_column=True)
            ```

        Args:
            source: 央视 or 卫视
            verbose: 是否打印日志
            logger: 自定义日志
            **kwargs: 其他参数
        """
        self.source = source
        self.mapping = TVMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs
        self.request_set(
            response_type="json",
            description="实时电视收视率",
        )

    def types(self):
        """"""
        mapping = {"央视": 0, "卫视": 1}
        return mapping[self.source]

    def params(self) -> Dict:
        """
        :return:
        """
        params = {"type": self.types()}
        return self.base_param(update=params)
