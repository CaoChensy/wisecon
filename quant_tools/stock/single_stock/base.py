from pydantic import BaseModel


__all__ = [
    "Url",
    "url",
]


class Url(BaseModel):
    """"""
    signal_stock_get: str = "https://push2.eastmoney.com/api/qt/stock/get"
    signal_stock_sse: str = "https://push2.eastmoney.com/api/qt/stock/sse"


url = Url()
