from typing import Dict, Optional, List, Literal
from wisecon.types import (
    BaseMapping,
    APICListRequestData,
    APIStockFFlowDayLineRequestData,
    APIUListNPRequestData,
)
from wisecon.utils import time2int


__all__ = [
    "TypeMarket",
    "CapitalFlowMapping",
    "CapitalFlowRequestData",
    "CapitalFlowHistoryBaseMapping",
    "CapitalFlowHistoryRequestData",
    "CapitalFlowCurrentBaseMapping",
    "CapitalFlowCurrentRequestData",
]


TypeMarket = Literal["全部股票", "沪深A股", "沪市A股", "科创板", "深市A股", "创业板", "沪市B股", "深市B股"]


class CapitalFlowMapping(BaseMapping):
    """字段映射 当前资金流量统计"""
    columns: Dict = {
        "f1": "",
        "f2": "最新价",
        "f3": "今日涨跌幅",
        "f12": "代码",
        "f13": "",
        "f14": "名称",
        "f62": "今日主力净流入(净额)",
        "f66": "今日超大单净流入(净额)",
        "f69": "今日超大单净流入(净占比)",
        "f72": "今日大单净流入(净额)",
        "f75": "今日大单净流入(净占比)",
        "f78": "今日中单净流入(净额)",
        "f81": "今日中单净流入(净占比)",
        "f84": "今日小单净流入(净额)",
        "f87": "今日小单净流入(净占比)",
        "f100": "行业名称",
        "f109": "5日涨跌幅",
        "f124": "",
        "f127": "3日涨跌幅",
        "f160": "10日涨跌幅",
        "f164": "5日主力净流入(净额)",
        "f165": "5日主力净流入(净占比)",
        "f166": "5日超大单净流入(净额)",
        "f167": "5日超大单净流入(净占比)",
        "f168": "5日大单净流入(净额)",
        "f169": "5日大单净流入(净占比)",
        "f170": "5日中单净流入(净额)",
        "f171": "5日中单净流入(净占比)",
        "f172": "5日小单净流入(净额)",
        "f173": "5日小单净流入(净占比)",
        "f174": "10日主力净流入(净额)",
        "f175": "10日主力净流入(净占比)",
        "f176": "10日超大单净流入(净额)",
        "f177": "10日超大单净流入(净占比)",
        "f178": "10日大单净流入(净额)",
        "f179": "10日大单净流入(净占比)",
        "f180": "10日中单净流入(净额)",
        "f181": "10日中单净流入(净占比)",
        "f182": "10日小单净流入(净额)",
        "f183": "10日小单净流入(净占比)",
        "f184": "今日主力净流入(占比)",
        "f204": "最大流入股票名称",
        "f205": "最大流入股票代码",
        "f206": "最大流入股票排名",
        "f225": "今日排名",
        "f257": "",
        "f258": "",
        "f259": "",
        "f260": "",
        "f261": "",
        "f263": "5日排名",
        "f264": "10日排名",
        "f265": "所属板块",
        "f267": "3日主力净流入(净额)",
        "f268": "3日主力净流入(净占比)",
        "f269": "3日超大单净流入(净额)",
        "f270": "3日超大单净流入(净占比)",
        "f271": "3日大单净流入(净额)",
        "f272": "3日大单净流入(净占比)",
        "f273": "3日中单净流入(净额)",
        "f274": "3日中单净流入(净占比)",
        "f275": "3日小单净流入(净额)",
        "f276": "3日小单净流入(净占比)",
    }


class CapitalFlowRequestData(APICListRequestData):
    """查询 当前资金流量统计"""
    sort_by: Optional[str]
    days: Optional[Literal[1, 3, 5, 10]]

    def base_param(self, update: Dict) -> Dict:
        """"""
        params = {}
        params.update(update)
        return params

    def params_sort_by(self) -> str:
        """"""
        days_mapping = {
            10: "f174",
            5: "f164",
            3: "f267",
            1: "f62",
        }
        if self.sort_by is None:
            if self.days in days_mapping:
                return days_mapping[self.days]
            else:
                return days_mapping[1]
        else:
            return self.sort_by

    def params_fields(self):
        """"""
        fields_mapping = {
            10: "f12,f14,f2,f160,f174,f175,f176,f177,f178,f179,f180,f181,f182,f183,f260,f261,f124,f1,f13",
            5: "f12,f14,f2,f109,f164,f165,f166,f167,f168,f169,f170,f171,f172,f173,f257,f258,f124,f1,f13",
            3: "f12,f14,f2,f127,f267,f268,f269,f270,f271,f272,f273,f274,f275,f276,f257,f258,f124,f1,f13",
            1: "f12,f14,f2,f3,f62,f184,f66,f69,f72,f75,f78,f81,f84,f87,f204,f205,f124,f1,f13",
            "f184": "f2,f3,f12,f13,f14,f62,f184,f225,f165,f263,f109,f175,f264,f160,f100,f124,f265,f1",
        }
        if self.days in fields_mapping:
            return fields_mapping[self.days]
        elif self.sort_by == "f184":
            return fields_mapping[self.sort_by]
        else:
            return fields_mapping[1]


class CapitalFlowHistoryBaseMapping(BaseMapping):
    """字段映射 历史资金流量统计"""
    fields: List = [
        "日期", "主力净流入净额", "小单净流入净额", "中单净流入净额", "大单净流入净额", "超大单净流入净额",
        "主力净流入净占比", "小单净流入净占比", "中单净流入净占比", "大单净流入净占比", "超大单净流入净占比",
        "收盘价", "涨跌幅", "a", "b"
    ]
    columns: Dict = {
        "f1": "日期",
        "f2": "主力净流入净额",
        "f3": "小单净流入净额",
        "f7": "中单净流入净额",
        "f51": "大单净流入净额",
        "f52": "超大单净流入净额",
        "f53": "主力净流入净占比",
        "f54": "小单净流入净占比",
        "f55": "中单净流入净占比",
        "f56": "大单净流入净占比",
        "f57": "超大单净流入净占比",
        "f58": "上证收盘价",
        "f59": "上证涨跌幅",
        "f60": "深证收盘价",
        "f61": "深证涨跌幅",
        "f62": "f62",
        "f63": "f63",
        "f64": "f64",
        "f65": "f65",
    }


class CapitalFlowHistoryRequestData(APIStockFFlowDayLineRequestData):
    """查询 历史资金流量统计"""
    sort_by: Optional[str]
    days: Optional[Literal[1, 3, 5, 10]]

    def base_param(self, update: Dict) -> Dict:
        """"""
        params = {
            "lmt": 0,
            "klt": 101,
            "fields1": "f1,f2,f3,f7",
            "fields2": "f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61,f62,f63,f64,f65",
            "_": time2int()
        }
        params.update(update)
        return params


class CapitalFlowCurrentBaseMapping(BaseMapping):
    """字段映射 当前资金流量统计"""
    columns: Dict = {
        "f6": "金额",
        "f62": "今日主力净流入(净额)",
        "f64": "超大单流入",
        "f65": "超大单流出",
        "f66": "今日超大单净流入(净额)",
        "f69": "今日超大单净流入(净占比)",

        "f70": "大单流入",
        "f71": "大单流出",
        "f72": "今日大单净流入(净额)",
        "f75": "今日大单净流入(净占比)",

        "f76": "中单流入",
        "f77": "中单流出",
        "f78": "今日中单净流入(净额)",
        "f81": "今日中单净流入(净占比)",

        "f82": "小单流入",
        "f83": "小单流出",
        "f84": "今日小单净流入(净额)",
        "f87": "今日小单净流入(净占比)",
        "f124": "",
        "f164": "一周主力净流入",
        "f166": "一周超大单净流入",
        "f168": "一周大单净流入",
        "f170": "一周中单净流入",
        "f172": "一周小单净流入",
        "f184": "今日主力净流入(占比)",
        "f252": "一月主力净流入",
        "f253": "一月超大单净流入",
        "f254": "一月大单净流入",
        "f255": "一月中单净流入",
        "f256": "一月小单净流入",
        "f278": "",
        "f279": "",
        "f280": "",
        "f281": "",
        "f282": "",
    }


class CapitalFlowCurrentRequestData(APIUListNPRequestData):
    """查询 当前资金流量统计"""

    def base_param(self, update: Dict) -> Dict:
        """"""
        fields = [
            "f62", "f184", "f66", "f69", "f72", "f75", "f78", "f81",
            "f84", "f87", "f64", "f65", "f70", "f71", "f76", "f77",
            "f82", "f83", "f164", "f166", "f168", "f170", "f172", "f252",
            "f253", "f254", "f255", "f256", "f124", "f6", "f278", "f279",
            "f280", "f281", "f282"
        ]
        params = {
            "fields": ",".join(fields),
            "fltt": 2,
            "_": time2int()
        }
        params.update(update)
        return params
