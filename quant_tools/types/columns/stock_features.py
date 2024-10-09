from typing import Optional, Union, List, Dict
from pydantic import BaseModel, Field


__all__ = [
    "StockFeatures"
]


class StockFeatures(BaseModel):
    """
    Stock features
    """
    # f1: Optional[Union[int, float]] = Field(default=None, description="open")
    # f2: Optional[Union[int, float]] = Field(default=None, description="close")
    # f3: Optional[Union[int, float]] = Field(default=None, description="high")
    # f4: Optional[Union[int, float]] = Field(default=None, description="low")
    # f5: Optional[Union[int, float]] = Field(default=None, description="涨跌幅")
    # f6: Optional[Union[int, float]] = Field(default=None, description="涨跌额")
    # f7: Optional[Union[int, float]] = Field(default=None, description="买五(价格)")
    # f8: Optional[Union[int, float]] = Field(default=None, description="买五(价格)")
    # f9: Optional[Union[int, float]] = Field(default=None, description="买五(价格)")
    # f10: Optional[Union[int, float]] = Field(default=None, description="买五(价格)")

    f11: Optional[Union[int, float]] = Field(default=None, description="买五(价格)")
    f12: Optional[Union[int, float]] = Field(default=None, description="买五(数量)")
    f13: Optional[Union[int, float]] = Field(default=None, description="买四(价格)")
    f14: Optional[Union[int, float]] = Field(default=None, description="买四(数量)")
    f15: Optional[Union[int, float]] = Field(default=None, description="买三(价格)")
    f16: Optional[Union[int, float]] = Field(default=None, description="买三(数量)")
    f17: Optional[Union[int, float]] = Field(default=None, description="买二(价格)")
    f18: Optional[Union[int, float]] = Field(default=None, description="买二(数量)")
    f19: Optional[Union[int, float]] = Field(default=None, description="买一(价格)")
    f20: Optional[Union[int, float]] = Field(default=None, description="买一(数量)")
    f31: Optional[Union[int, float]] = Field(default=None, description="卖五(价格)")
    f32: Optional[Union[int, float]] = Field(default=None, description="卖五(数量)")
    f33: Optional[Union[int, float]] = Field(default=None, description="卖四(价格)")
    f34: Optional[Union[int, float]] = Field(default=None, description="卖四(数量)")
    f35: Optional[Union[int, float]] = Field(default=None, description="卖三(价格)")
    f36: Optional[Union[int, float]] = Field(default=None, description="卖三(数量)")
    f37: Optional[Union[int, float]] = Field(default=None, description="卖二(价格)")
    f38: Optional[Union[int, float]] = Field(default=None, description="卖二(数量)")
    f39: Optional[Union[int, float]] = Field(default=None, description="卖一(价格)")
    f40: Optional[Union[int, float]] = Field(default=None, description="卖一(数量)")
    f43: Optional[Union[int, float]] = Field(default=None, description="最新")
    f44: Optional[Union[int, float]] = Field(default=None, description="最高")
    f45: Optional[Union[int, float]] = Field(default=None, description="最低")
    f46: Optional[Union[int, float]] = Field(default=None, description="今开")
    f47: Optional[Union[int, float]] = Field(default=None, description="总手")
    f48: Optional[float] = Field(default=None, description="金额")
    f49: Optional[float] = Field(default=None, description="外盘")
    f50: Optional[Union[int, float]] = Field(default=None, description="量比")
    f51: Optional[Union[int, float]] = Field(default=None, description="涨停")
    f52: Optional[Union[int, float]] = Field(default=None, description="跌停")
    f57: Optional[str] = Field(default=None, description="股票代码")
    f58: Optional[str] = Field(default=None, description="股票简称")
    # f59: 2,
    f60: Optional[str] = Field(default=None, description="昨收")
    f71: Optional[str] = Field(default=None, description="均价")
    f84: Optional[Union[int, float]] = Field(default=None, description="总股本")
    f85: Optional[Union[int, float]] = Field(default=None, description="流通股")
    # f86: 1727681655,
    f92: Optional[float] = Field(default=None, description="每股净资产")
    # f107: 0,
    # f108: 1.288050952,
    # f111: 80,
    # f116: 24551601900.0,
    # f117: 6137910000.0,
    # f152: 2,
    # f161: Optional[Union[int, float]] Field(default=None, description="涨跌") 62498,
    f162: Optional[Union[int, float]] = Field(default=None, description="PE(动态:总市值除以全年预估净利润,例如当前一季度净利润1000万,则预估全年净利润4000万)")
    f163: Optional[Union[int, float]] = Field(default=None, description="PE(静态:总市值除以上一年度净利润)")
    f164: Optional[Union[int, float]] = Field(default=None, description="PE(滚动:最新价除以最近4个季度的每股收益)")
    f167: Optional[Union[int, float]] = Field(default=None, description="市净")
    f168: Optional[Union[int, float]] = Field(default=None, description="换手")
    f169: Optional[Union[int, float]] = Field(default=None, description="涨跌")
    f170: Optional[Union[int, float]] = Field(default=None, description="涨幅")
    f171: Optional[Union[int, float]]= Field(default=None, description="振幅")
    # f177: 72,
    f191: Optional[Union[int, float]] = Field(default=None, description="委比")
    f192: Optional[Union[int, float]] = Field(default=None, description="委差")
    # f256: -,
    # f257: 0,
    # f260: 12,
    # f261: 457200.0,
    # f262: -,
    # f269: -,
    # f270: 0,
    # f277: 64439900.0,
    # f278: 16110000.0,
    # f279: 1,
    # f285: -,
    # f286: 0,
    # f288: 0,
    # f292: 13,
    # f294: 1,
    # f295: 0,
    # f301: 38100,
    f531: Optional[Union[int, float]] = Field(default=None, description="f531")
    # f734: N长联科技,
    # f747: -,
    # f748: 0,

    # def mapping(self):
    #     """"""
    #     properties = self.model_json_schema().get("properties")
    #     mapping = dict()

    def _mapping(self, columns: List[str]) -> Dict:
        """"""
        properties = self.model_json_schema().get("properties")
        mapping = dict()
        for column in columns:
            column_info = properties.get(column)
            if column_info is not None:
                description = column_info.get("description")
                mapping.update({column: description})
        return mapping

    def tick_columns(self) -> Dict:
        """"""
        columns = [
            "f11", "f12", "f13", "f14", "f15", "f16", "f17", "f18", "f19", "f20",
            "f31", "f32", "f33", "f34", "f35", "f36", "f37", "f38", "f39", "f40",
            "f191", "f192", "f531",
        ]
        columns_mapping = self._mapping(columns)
        return columns_mapping

    def company_core_columns(self):
        """"""
