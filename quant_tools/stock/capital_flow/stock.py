from pydantic import Field
from typing import Any, Dict, Literal, Callable, Optional
from zlai.types.tools import ResponseData, BaseRequestData, BaseRequestConfig


__all__ = [
    "StockFlowQueryConfig",
    "StockFlow",
]


TypeMarketCode = Literal["全部股票", "沪深A股", "沪市A股", "科创板", "深市A股", "创业板", "沪市B股", "深市B股"]


class StockFlowQueryConfig(BaseRequestConfig):
    """"""
    market: Optional[TypeMarketCode] = Field(default="全部股票")
    days: Optional[int] = Field(default=1)
    size: Optional[int] = Field(default=50)
    sort_by: Optional[str] = Field(default=None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _market_mapping(self) -> str:
        """"""
        market_mapping = {
            "全部股票": "m:0+t:6+f:!2,m:0+t:13+f:!2,m:0+t:80+f:!2,m:1+t:2+f:!2,m:1+t:23+f:!2,m:0+t:7+f:!2,m:1+t:3+f:!2",
            "沪深A股": "m:0+t:6+f:!2,m:0+t:13+f:!2,m:0+t:80+f:!2,m:1+t:2+f:!2,m:1+t:23+f:!2",
            "沪市A股": "m:1+t:2+f:!2,m:1+t:23+f:!2",
            "科创板": "m:1+t:23+f:!2",
            "深市A股": "m:0+t:6+f:!2,m:0+t:13+f:!2,m:0+t:80+f:!2",
            "创业板": "m:0+t:80+f:!2",
            "沪市B股": "m:1+t:3+f:!2",
            "深市B股": "m:0+t:7+f:!2"
        }
        if self.market in market_mapping:
            return market_mapping[self.market]
        else:
            return market_mapping["全部股票"]

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
            "fs": self._market_mapping(),
            "fields": fields,
        }
        return params


class StockFlow(BaseRequestData):
    """"""
    def __init__(
            self,
            query_config: Optional[StockFlowQueryConfig] = None,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        """
        :param market:
            Literal["全部股票", "沪深A股", "沪市A股", "科创板", "深市A股", "创业板", "沪市B股", "深市B股"]
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
            self.query_config = StockFlowQueryConfig.model_validate(kwargs)
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
            "description": "个股资金流向历史数据(沪深两市)",
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
