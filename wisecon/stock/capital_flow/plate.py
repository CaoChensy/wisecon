from pydantic import Field
from typing import Any, Dict, Literal, Callable, Optional
from zlai.types.tools import ResponseData, BaseRequestData, BaseRequestConfig


__all__ = [
    "PlateFlowQueryConfig",
    "PlateFlow",
]


TypePlate = Literal["行业", "概念", "地区"]


class PlateFlowQueryConfig(BaseRequestConfig):
    """"""
    plate: Optional[TypePlate] = Field(default="行业", description="板块类型")
    size: Optional[int] = Field(default=50)
    sort_by: Optional[str] = Field(default=None)
    days: Optional[int] = Field(default=1)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _plate_mapping(self) -> str:
        """
        :return:
        """
        plate_mapping = {
            "行业": "m:90+t:2",
            "概念": "m:90+t:3",
            "地区": "m:90+t:1",
        }
        if self.plate in plate_mapping:
            return plate_mapping[self.plate]
        else:
            return plate_mapping["行业"]

    def _sort_by_mapping(self) -> str:
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

    def _fields_mapping(self):
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

    def params(self) -> Dict:
        """"""
        sort_by = self._sort_by_mapping()
        fields = self._fields_mapping()

        if sort_by not in fields:
            raise ValueError(f"Invalid sort_by value, please check the value in the `fields` attribute. {fields}")

        params = {
            "fid": sort_by,
            "po": 1,
            "pz": self.size,
            "pn": 1,
            "np": 1,
            "fltt": 2,
            "invt": 2,
            "fs": self._plate_mapping(),
            "fields": fields,
        }
        return params


class PlateFlow(BaseRequestData):
    """"""
    def __init__(
            self,
            query_config: Optional[PlateFlowQueryConfig] = None,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        """
        :param plate:
            Literal["行业", "概念", "地区"]
        :param days:
            Literal[1, 3, 5, 10]
        :param sort_by:
            - all:
                "f2": "最新价",
                "f3": "今日涨跌幅",
                "f12": "代码",
                "f14": "名称",
            - 1days:
                "f3": "今日涨跌幅",
                "f62": "今日主力净流入(净额)",
                "f184": "今日主力净流入(占比)",
                "f66": "今日超大单净流入(净额)",
                "f69": "今日超大单净流入(净占比)",
                "f72": "今日大单净流入(净额)",
                "f75": "今日大单净流入(净占比)",
                "f78": "今日中单净流入(净额)",
                "f81": "今日中单净流入(净占比)",
                "f84": "今日小单净流入(净额)",
                "f87": "今日小单净流入(净占比)",
            - 3days:
                "f127": "3日涨跌幅",
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
            - 5days:
                "f109": "5日涨跌幅",
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
            - 10days:
                "f160": "10日涨跌幅",
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
        :param size: 默认 50
        :param query_config:
        :param verbose:
        :param logger:
        :param kwargs:
        """
        if query_config is None:
            self.query_config = PlateFlowQueryConfig.model_validate(kwargs)
        else:
            self.query_config = query_config
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs

    def _base_url(self) -> str:
        """"""
        base_url = "https://push2.eastmoney.com/api/qt/clist/get"
        return base_url

    def load_data(self) -> ResponseData:
        """
        指标定义
        　　- 超大单：大于等于50万股或者100万元的成交单;
        　　- 大单：大于等于10万股或者20万元且小于50万股和100万元的成交单;
        　　- 中单：大于等于2万股或者4万元且小于10万股和20万元的成交单;
        　　- 小单：小于2万股和4万元的成交单;
        　　- 流入：买入成交额;
        　　- 流出：卖出成交额;
        　　- 主力流入：超大单加大单买入成交额之和;
        　　- 主力流出：超大单加大单卖出成交额之和;
        　　- 净额：流入-流出;
        　　- 净比：(流入-流出)/总成交额;
        　　- 5日排名：5日主力净占比排名（指大盘连续交易的5日);
        　　- 5日涨跌：最近5日涨跌幅（指大盘连续交易的5日);
        　　- 10日排名：10日主力净占比排名（指大盘连续交易的10日);
        　　- 10日涨跌：最近10日涨跌幅（指大盘连续交易的10日);

        :return:
        """
        metadata = self.request_json().get("data", {})
        data = metadata.pop("diff")
        self.update_metadata(metadata)
        self._logger(msg=f"[{__class__.__name__}] Find {len(data)} reports.", color="green")
        return ResponseData(data=data, metadata=metadata)

    def update_metadata(self, metadata: Dict):
        """"""
        metadata.update({
            "description": "板块（行业、概念、地区）资金流向历史数据(沪深两市)",
            "columns": {
                # "f1": "",
                "f2": "最新价",
                "f3": "今日涨跌幅",
                "f12": "代码",
                # "f13": "",
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
                # "f124": "",
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
                # "f204": "",
                # "f205": "",
                # "f206": "",
                # "f257": "",
                # "f258": "",
                # "f259": "",
                # "f260": "",
                # "f261": "",
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
            },
        })
