import pandas as pd
from typing import Any, Optional, Literal
from wisecon.stock.kline import KLine
from wisecon.utils import LoggerMixin
from wisecon.utils.time import get_now_date, days_between_dates, date_add_subtract


__all__ = [
    "UpdateKline",
]


class UpdateKline(LoggerMixin):
    """Update kline"""
    date: str
    if_exists: Literal["replace", "append"]
    max_date: Optional[str]

    def __init__(
            self,
            conn: Any,
            current_date: Optional[bool] = False,
            verbose: Optional[bool] = False,
            **kwargs,
    ):
        """"""
        self.conn = conn
        self.current_date = current_date
        self.verbose = verbose
        self.kwargs = kwargs

    def __call__(
            self,
            security_code: Optional[str] = None,
            market_code: Optional[str] = None,
            date: Optional[str] = None,
            *args,
            **kwargs
    ):
        """"""
        self.date = self.validate_current_date(date)
        code = security_code if security_code else market_code
        self.validate(code)
        self.fetch_data(security_code=security_code, market_code=market_code)

    def validate_current_date(self, date: Optional[str] = None) -> str:
        """"""
        if date:
            return date
        else:
            now_date = get_now_date(format="%Y-%m-%d")
            if self.current_date:
                return now_date
            else:
                return date_add_subtract(date_str=now_date, days=-1)

    def validate(self, code):
        """"""
        exist_codes = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table'", con=self.conn)

        if code not in exist_codes.values:
            self.if_exists = "replace"
            self.max_date = None
            self.info(msg=f"[{__class__.__name__}] Find new code: {code}")
        else:
            cnt = pd.read_sql_query(f"SELECT count(*) AS cnt FROM `{code}`", con=self.conn).values[0][0]
            if cnt == 0:
                self.if_exists = "replace"
                self.max_date = None
            else:
                self.if_exists = "append"
                _df_date = pd.read_sql_query(f"SELECT max(time) AS max_date FROM `{code}`", con=self.conn)
                self.max_date = str(_df_date.values[0][0])
            self.info(msg=f"[{__class__.__name__}] `{code}` has {cnt} length, max date is {self.max_date}")

    def fetch_data(self, security_code: Optional[str], market_code: Optional[str]):
        """"""
        if self.max_date is None or self.date > self.max_date:
            if self.max_date is None:
                size = 200
                data_time_range = ["1949-10-01", self.date]
            else:
                size = days_between_dates(self.max_date, self.date)
                data_time_range = [self.max_date, self.date]

            kline = KLine(security_code=security_code, market_code=market_code, period="1D", size=size)
            df_data = kline.load().to_frame()

            if len(df_data) == 0:
                self.info(msg=f"[{__class__.__name__}] {security_code} {self.max_date} to {self.date} no data")
            else:
                code = security_code if security_code else market_code
                df_data = df_data[df_data["time"].between(*data_time_range)]
                df_data.to_sql(code, con=self.conn, if_exists=self.if_exists, index=False)
                self.info(msg=f"[{__class__.__name__}] {code} {self.max_date} to {self.date}, update {len(df_data)}")
        else:
            self.info(msg=f"[{__class__.__name__}] data already exists, skip update")
