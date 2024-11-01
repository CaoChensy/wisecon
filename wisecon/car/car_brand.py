from typing import Any, Dict, Callable, Optional, Literal, List
from wisecon.types import BaseMapping, APICurrentCarRequestData


__all__ = [
    "CarBrandListMapping",
    "CarBrandList",
]


class CarBrandListMapping(BaseMapping):
    """字段映射 汽车品牌列表"""
    columns: Dict = {
        "cat_id": "id",
        "alpha": "alpha",
        "title": "name",
        "key": "key",
    }


class CarBrandList(APICurrentCarRequestData):
    """查询 汽车品牌列表"""
    def __init__(
            self,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        """
        Notes:
            ```python
            data = CarBrandList().load()
            data.to_frame(chinese_column=True)
            ```

        Args:
            verbose: 是否打印日志
            logger: 自定义日志打印函数
            **kwargs: 其他参数
        """
        self.mapping = CarBrandListMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs
        self.request_set(description="汽车品牌列表")

    def clean_json(
            self,
            json_data: Optional[Dict],
    ) -> List[Dict]:
        """"""
        data = json_data.pop("data")
        self.metadata.response = json_data

        def clean_item(item: Dict) -> List:
            """"""
            d = item.get("list")
            k = item.get("key")
            [_item.update({"key": k}) for _item in d]
            return d

        data = list(map(clean_item, data))
        return sum(data, [])

    def params(self) -> Dict:
        """"""
        params = {"extra": "getCarBrand",}
        return self.base_param(update=params)
