from typing import Dict, Optional, List, Literal
from wisecon.types import BaseRequestData, BaseMapping


__all__ = [
    "CapitalFlowMapping",
    "CapitalFlowRequestData",
]


class CapitalFlowMapping(BaseMapping):
    """"""
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
        "f204": "",
        "f205": "",
        "f206": "",
        "f257": "",
        "f258": "",
        "f259": "",
        "f260": "",
        "f261": "",
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


class CapitalFlowRequestData(BaseRequestData):
    """"""
    sort_by: Optional[str]
    days: Optional[Literal[1, 3, 5, 10]]

    def base_url(self) -> str:
        """"""
        base_url = "https://push2.eastmoney.com/api/qt/clist/get"
        return base_url

    def base_param(self, update: Dict) -> Dict:
        """"""
        params = {}
        params.update(update)
        return params

    def clean_json(
            self,
            json_data: Optional[Dict],
    ) -> List[Dict]:
        """"""
        response = json_data.get("data", {})
        data = response.pop("diff")
        self.metadata.response = response
        return data

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
        }
        if self.days in fields_mapping:
            return fields_mapping[self.days]
        else:
            return fields_mapping[1]

