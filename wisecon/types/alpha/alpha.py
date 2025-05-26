import pandas as pd
from pydantic import BaseModel, ConfigDict
from typing import List, Optional


__all__ = [
    "AlphaKlineData",
]


class AlphaKlineData(BaseModel):
    """Alpha101 K线数据"""
    model_config = ConfigDict(arbitrary_types_allowed=True)
    open: Optional[pd.DataFrame] = None
    close: Optional[pd.DataFrame] = None
    high: Optional[pd.DataFrame] = None
    low: Optional[pd.DataFrame] = None
    volume: Optional[pd.DataFrame] = None
    turnover: Optional[pd.DataFrame] = None
    cap: Optional[pd.DataFrame] = None

    def __init__(self, data: List[pd.DataFrame] = None, codes: List[str] = None, **kwargs):
        """"""
        super().__init__(**kwargs)
        self.merge(data, codes)

    def merge(self, data: List[pd.DataFrame] = None, codes: List[str] = None):
        """"""
        _open = []
        _close = []
        _high = []
        _low = []
        _volume = []
        _turnover = []

        for _data, code in zip(data, codes):
            _open.append(_data["open"].rename(code).astype(float))
            _close.append(_data["close"].rename(code).astype(float))
            _high.append(_data["high"].rename(code).astype(float))
            _low.append(_data["low"].rename(code).astype(float))
            _volume.append(_data["volume"].rename(code).astype(float))
            _turnover.append(_data["turnover"].rename(code).astype(float))

        self.open = pd.concat(_open, axis=1).fillna("ffill")
        self.close = pd.concat(_close, axis=1).fillna("ffill")
        self.high = pd.concat(_high, axis=1).fillna("ffill")
        self.low = pd.concat(_low, axis=1).fillna("ffill")
        self.volume = pd.concat(_volume, axis=1).fillna("ffill")
        self.turnover = pd.concat(_turnover, axis=1).fillna("ffill")
