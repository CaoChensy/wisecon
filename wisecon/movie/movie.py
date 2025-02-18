from typing import Any, Dict, Callable, Optional, Annotated
from wisecon.types import BaseMapping
from wisecon.types.request_api.movie import APIMovieRequestData


__all__ = [
    "MovieMapping",
    "Movie",
]


class MovieMapping(BaseMapping):
    """字段映射 当前实时电影票房"""
    columns: Dict = {
        "boxDesc": "票房描述",
        "boxRate": "票房占比",
        "movieId": "电影ID",
        "movieName": "电影名称",
        "releaseInfo": "上映信息",
        "seatCountRate": "座位使用率",
        "showCountRate": "场次占比",
        "sumBoxDesc": "总票房描述"
    }


class Movie(APIMovieRequestData):
    """查询 当前实时电影票房"""
    def __init__(
            self,
            verbose: Annotated[Optional[bool], "", False] = False,
            logger: Annotated[Optional[Callable], "", False] = None,
            **kwargs: Annotated[Any, "", False],
    ):
        """
        Notes:
            ```python
            from wisecon.movie import *

            # 查询 当前实时电影票房
            data = Movie().load()
            data.to_frame(chinese_column=True)
            ```

        Args:
            verbose: 是否打印日志
            logger: 自定义日志
            **kwargs: 其他参数
        """
        self.mapping = MovieMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs
        self.request_set(
            response_type="json",
            description="电影票房",
        )

    def params(self) -> Dict:
        """
        :return:
        """
        params = {}
        return self.base_param(update=params)
