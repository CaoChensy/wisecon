import time
import requests
import pandas as pd
from typing import Any, Dict, Callable, Optional
from wisecon.types.headers import headers
from wisecon.types import ResponseData, BaseMapping, APIConceptionBK, APICListRequestData


__all__ = [
    "ConceptionMap",
    "ListConceptionStock",
]


class ConceptionMap(APIConceptionBK):
    """"""
    mapping_code: Dict[str, str] = {
        "地域板块": "020",
        "行业板块": "016",
        "概念板块": "007",
    }

    def __init__(self):
        """"""
        self.map_industry = self.list_industry()
        self.map_conception = self.list_conception()
        self.map_district = self.list_district()
        self.mapping_data = sum([
            self.map_conception.data, self.map_industry.data, self.map_district.data
        ], [])

    def _get_data(self, params: Dict) -> ResponseData:
        """"""
        response = requests.get(self.base_url(), params=params, headers=headers.headers)
        metadata = response.json()
        data = metadata.pop("data")
        return ResponseData(data=data, metadata=metadata)

    def list_industry(self, ) -> ResponseData:
        """"""
        params = {"bkCode": "016", "_": str(int(time.time() * 1E3))}
        return self._get_data(params)

    def list_conception(self) -> ResponseData:
        """"""
        params = {"bkCode": "007", "_": str(int(time.time() * 1E3))}
        return self._get_data(params)

    def list_district(self) -> ResponseData:
        """"""
        params = {"bkCode": "020", "_": str(int(time.time() * 1E3))}
        return self._get_data(params)

    def get_code_by_name(self, name: str) -> pd.DataFrame:
        """"""
        df = pd.DataFrame(self.mapping_data)
        return df.loc[df.bkName.str.contains(name), ["bkCode", "bkName"]]

    def get_name_by_code(self, code: str) -> pd.DataFrame:
        """"""
        df = pd.DataFrame(self.mapping_data)
        return df.loc[df.bkCode == code, ["bkCode", "bkName"]]


class ListConceptionMapping(BaseMapping):
    """字段映射 板块下的股票列表"""
    columns: Dict = {
        "f12": "证券代码",
        "f14": "证券名称",
    }


class ListConceptionStock(APICListRequestData):
    """板块下的股票列表"""
    def __init__(
            self,
            bk_code: str,
            sort_by: Optional[str] = "f12",
            page_size: Optional[int] = 50,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        """
        Notes:
            ```python
            from wisecon.stock.market import *

            # 查询ETF市场当前行情
            data = CurrentMarket(market="ETF",).load()
            data.to_frame(chinese_column=True)
            ```

        Args:
            bk_code: 板块代码
            sort_by: 排序字段
            page_size: 每页数据量
            verbose: 是否打印日志
            logger: 自定义日志打印函数
            **kwargs: 其他参数
        """
        self.bk_code = bk_code
        self.sort_by = sort_by
        self.page_size = page_size
        self.mapping = ListConceptionMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs
        self.request_set(description="板块下的股票列表")

    def params(self) -> Dict:
        """"""
        params = {
            "pn": 1,
            "pz": self.page_size,
            "fid": self.sort_by,
            "fs": f"b:{self.bk_code}",
            "fields": "f12,f14",
        }
        return self.base_param(update=params)
