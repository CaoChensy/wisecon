import duckdb
import warnings
import pandas as pd
from typing import Callable, Literal, Optional
from wisecon.utils.logger import LoggerMixin
from duckdb_engine import DuckDBEngineWarning
warnings.filterwarnings("ignore", category=DuckDBEngineWarning)


__all__ = ["DuckDB"]


class DuckDB(LoggerMixin):
    def __init__(
            self,
            database: str,
            logger: Optional[Callable] = None,
            verbose: Optional[bool] = None,
            **kwargs,
    ):
        self.conn = duckdb.connect(database=database, **kwargs)
        self.logger = logger
        self.verbose = verbose

    def execute(self, query: str):
        return self.conn.execute(query).fetchall()

    def close(self):
        self.conn.close()

    def save_dataframe(
            self,
            df: pd.DataFrame,
            name: str,
            if_exists: Literal["fail", "replace", "append"] = "replace",
    ) -> None:
        """"""
        df.to_sql(name=name, con=self.conn, if_exists=if_exists, index=False)

