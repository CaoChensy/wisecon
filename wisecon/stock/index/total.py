from typing import Any, Dict, Callable, Optional, Literal
from wisecon.types import BaseMapping, APICListRequestData


__all__ = [
    "ListALLStockMapping",
    "ListALLStock",
]


TypeMarket = Literal[
    "沪深京A股",
    "上证A股", "注册制上证A股", "核准制上证A股",
    "深证A股", "注册制深证A股", "核准制深证A股",
    "创业板", "注册制创业板", "核准制创业板",
    "北证A股", "新股", "科创板", "沪股通", "深股通", "B股",
    "上证AB股比价", "深证AB股比价",
    "风险警示板", "风险警示板(SH)", "风险警示板(SZ)", "风险警示板(科创)", "风险警示板(创业)", "两网及退市",
    "ETF", "LOF", "封闭基金",
]


class ListALLStockMapping(BaseMapping):
    """字段映射 `ETF/LOF/Stock`当前市场行情"""
    columns: Dict = {
        "f1": "",
        "f2": "最新价",
        "f3": "涨跌幅",
        "f4": "涨跌额",
        "f5": "成交量",
        "f6": "成交额",
        "f7": "振幅",
        "f8": "换手率",
        "f9": "市盈率",
        "f10": "量比",
        "f12": "证券代码",
        "f13": "",
        "f14": "证券名称",
        "f15": "最高价",
        "f16": "最低价",
        "f17": "开盘价",
        "f18": "昨收",
        "f20": "总市值",
        "f21": "流通市值",
        "f23": "市净率",
        "f24": "60日涨跌幅",
        "f25": "今年涨跌幅",
        "f26": "上市时间",
        "f22": "涨速",
        "f11": "",
        "f62": "",
        "f128": "",
        "f136": "",
        "f115": "",
        "f152": "",
        "f140": "",
        "f141": "",
        "f195": "B股最新价",
        "f196": "",
        "f197": "B股涨跌幅",
        "f199": "比价(A/B)",
        "f200": "",
        "f201": "B股代码",
        "f202": "",
        "f203": "B股名称",
    }


class ListALLStock(APICListRequestData):
    """查询 `ETF/LOF/Stock`当前市场行情"""
    def __init__(
            self,
            market: TypeMarket,
            size: Optional[int] = None,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        """
        Notes:
            ```python
            from wisecon.stock.market import *

            # 查询ETF市场当前行情
            data = ListALLStock(market="ETF",).load()
            data.to_frame(chinese_column=True)

            # 查询LOF市场当前行情
            data = ListALLStock(market="LOF",).load()
            data.to_frame(chinese_column=True)

            # 查询封闭基金当前行情
            data = ListALLStock(market="封闭基金",).load()
            data.to_frame(chinese_column=True)

            # 查询沪深京A股当前行情
            data = ListALLStock(market="沪深京A股",).load()
            data.to_frame(chinese_column=True)
            ```

        Args:
            market: 市场类型: ```
                [
                    "沪深京A股",
                    "上证A股", "注册制上证A股", "核准制上证A股",
                    "深证A股", "注册制深证A股", "核准制深证A股",
                    "创业板", "注册制创业板", "核准制创业板",
                    "北证A股", "新股", "科创板", "沪股通", "深股通", "B股",
                    "上证AB股比价", "深证AB股比价",
                    "风险警示板", "风险警示板(SH)", "风险警示板(SZ)", "风险警示板(科创)", "风险警示板(创业)", "两网及退市",
                    "ETF", "LOF", "封闭基金",
                ]```
            sort_by: 排序字段
            page_size: 每页数据量
            page_number: 页码
            verbose: 是否打印日志
            logger: 自定义日志打印函数
            **kwargs: 其他参数
        """
        self.market = market
        self.size = size
        self.mapping = ListALLStockMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs
        self.request_set(description="`ETF/LOF/Stock`当前市场行情")

    def params_market(self) -> str:
        """"""
        market_mapping = {
            "沪深京A股": "m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23,m:0+t:81+s:2048",
            "上证A股": "m:1+t:2,m:1+t:23",
            "注册制上证A股": "m:1+t:2+s:131072,m:1+t:23+s:131072",
            "核准制上证A股": "m:1+t:2+s:524288,m:1+t:23+s:524288",
            "深证A股": "m:0+t:6,m:0+t:80",
            "注册制深证A股": "m:0+t:6+s:131072,m:0+t:80+s:131072",
            "核准制深证A股": "m:0+t:6+s:524288,m:0+t:80+s:524288",
            "北证A股": "m:0+t:81+s:2048",
            "新股": "m:0+f:8,m:1+f:8",
            "创业板": "m:0+t:80",
            "注册制创业板": "m:0+t:80+s:131072",
            "核准制创业板": "m:0+t:80+s:!131072",
            "科创板": "m:1+t:23",
            "沪股通": "b:BK0707",
            "深股通": "b:BK0804",
            "B股": "m:0+t:7,m:1+t:3",
            "上证AB股比价": "m:1+b:BK0498",
            "深证AB股比价": "m:0+b:BK0498",
            "风险警示板": "m:0+f:4,m:1+f:4",
            "风险警示板(SH)": "m:1+f:4",
            "风险警示板(SZ)": "m:0+f:4",
            "风险警示板(科创)": "m:1+t:23+f:4",
            "风险警示板(创业)": "m:0+t:80+f:4",
            "两网及退市": "m:0+s:3",
            "ETF": "b:MK0021,b:MK0022,b:MK0023,b:MK0024,b:MK0827",
            "LOF": "b:MK0404,b:MK0405,b:MK0406,b:MK0407",
            "封闭基金": "e:19",
        }
        return market_mapping[self.market]

    def params(self) -> Dict:
        """"""
        params = {
            "pn": 1,
            "pz": 20,
            "fid": "f12",
            "fs": self.params_market(),
            "fields": "f12,f14",
        }
        return self.base_param(update=params)
