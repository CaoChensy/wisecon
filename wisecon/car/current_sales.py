from typing import Any, Dict, Callable, Optional, Literal
from wisecon.types import BaseMapping, APICurrentCarRequestData


__all__ = [
    "CurrentCarSalesMapping",
    "CurrentCarSales",
]


class CurrentCarSalesMapping(BaseMapping):
    """字段映射 汽车当前销量排行榜"""
    columns: Dict = {
        "date": "日期",
        "num": "数量",
        "levelId": "级别ID",
        "level": "车型级别",
        "factoryId": "厂商ID",
        "title": "厂商名称",
        "styleId": "车型ID",
        "bodyId": "车身ID",
        "body": "车身类别",
        "brandId": "品牌ID",
    }


class CurrentCarSales(APICurrentCarRequestData):
    """查询 汽车当前销量排行榜"""
    def __init__(
            self,
            data_type: Literal["销量", "品牌销量", "厂商销量", "车型级别", "车身类别", "车型销量", "电动车销量"] = "销量",
            start_date: Optional[str] = None,
            end_date: Optional[str] = None,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        """
        Notes:
            ```python
            data = CurrentCarSales(data_type="电动车销量",).load()
            data.to_frame(chinese_column=True)
            ```

        Args:
            data_type: 查询类型
            start_date: 开始日期, %Y-%m
            end_date: 结束日期, %Y-%m
            verbose: 是否打印日志
            logger: 自定义日志打印函数
            **kwargs: 其他参数
        """
        self.data_type = data_type
        self.start_date = start_date
        self.end_date = end_date
        self.mapping = CurrentCarSalesMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs
        self.request_set(description="汽车当前销量排行榜")
        self.conditions = []
        self.validate_date_format(date=[start_date, end_date], _format="%Y-%m")

    def params_ranking(self) -> str:
        """"""
        rank_mapping = {
            "销量": "monthRanking",
            "车型级别": "levelRanking",
            "厂商销量": "factoryRanking",
            "车型销量": "styleRanking",
            "车身类别": "bodyRanking",
            "品牌销量": "brandRanking",
            "电动车销量": "evRanking",
        }
        return rank_mapping[self.data_type]

    def params(self) -> Dict:
        """"""
        params = {
            "extra": self.params_ranking(),
            "fromDate": self.start_date,
            "toDate": self.end_date,
        }
        params = self.params_drop_none(params=params)
        return self.base_param(update=params)
