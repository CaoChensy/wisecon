import pprint
import pandas as pd
from pydantic import BaseModel, Field
from typing import Any, List, Dict, Union, Literal, Optional


__all__ = [
    "Metadata",
    "ResponseData",
]


class Metadata(BaseModel):
    """"""
    columns: Dict[str, Any] = Field(default={})
    description: str = Field(default="")
    response: Dict[str, Any] = Field(default={})

    def __init__(self, **kwargs):
        """"""
        super().__init__(**kwargs)
        self.columns = {k: v for k, v in self.columns.items() if v}


class ResponseData(BaseModel):
    """"""
    metadata: Optional[Metadata] = Field(default=None)
    data: List[Dict] = Field(default=[])

    def __init__(
            self,
            data: List[Dict],
            metadata: Optional[Metadata] = None,
            **kwargs
    ):
        """"""
        super().__init__(**kwargs)
        self.data = data
        self.metadata = metadata

    def show_columns(self):
        """"""
        pprint.pprint(self.metadata.columns, indent=4)

    def _trans_chinese_columns(self, item: Dict) -> Dict:
        """"""
        return {self.metadata.columns.get(key, key): value for key, value in item.items()}

    def to_dict(
            self,
            chinese_column: Optional[bool] = False,
    ) -> List[Dict]:
        """
        Notes:
            TODO: 增加处理未解析字段的方法。

        Args:
            chinese_column:

        Returns:

        """
        if chinese_column:
            data = [self._trans_chinese_columns(item) for item in self.data]
        else:
            data = self.data
        return data

    def to_frame(
            self,
            chinese_column: Optional[bool] = False,
    ) -> pd.DataFrame:
        """"""
        df = pd.DataFrame(data=self.data)
        if chinese_column:
            df.rename(columns=self.metadata.columns, inplace=True)
        return df

    def to_markdown(
            self,
            chinese_column: Optional[bool] = False,
            **kwargs,
    ) -> str:
        """"""
        return self.to_frame(chinese_column).to_markdown(**kwargs)

    def to_csv(
            self,
            path: str,
            chinese_column: Optional[bool] = False,
            **kwargs: Any
    ) -> None:
        """"""
        self.to_frame(chinese_column).to_csv(path, **kwargs)

    def to_excel(
            self,
            path: str,
            chinese_column: Optional[bool] = False,
            **kwargs: Any
    ) -> None:
        """"""
        self.to_frame(chinese_column).to_excel(path, **kwargs)

    def to_parquet(
            self,
            path: str,
            chinese_column: Optional[bool] = False,
            index: Optional[bool] = False,
            engine: Literal["auto", "pyarrow", "fastparquet"] = "auto",
            compression: str | None = "snappy",
            **kwargs: Any
    ) -> None:
        self.to_frame(chinese_column).to_parquet(
            path, index=index, engine=engine,
            compression=compression, **kwargs)

    def to_pickle(
            self,
            path: str,
            chinese_column: Optional[bool] = False,
            **kwargs: Any,
    ):
        """"""
        self.to_frame(chinese_column).to_pickle(path,  **kwargs)

    def to_string(
            self,
            chinese_column: Optional[bool] = False,
            **kwargs
    ):
        """"""
        self.to_frame(chinese_column).to_string(**kwargs)

    def to_sql(
            self,
            name: str,
            con,
            chinese_column: Optional[bool] = False,
            if_exists: Literal["fail", "replace", "append"] = "fail",
            index: Optional[bool] = True,
            **kwargs
    ):
        """"""
        self.to_frame(chinese_column).to_sql(
            name=name, con=con, if_exists=if_exists,
            index=index, **kwargs)

    def to_duckdb(
            self,
            database: str,
            name: str,
            chinese_column: Optional[bool] = False,
            if_exists: Literal["fail", "replace", "append"] = "replace",
            **kwargs,
    ):
        """"""
        from sqlalchemy import create_engine

        df = self.to_frame(chinese_column)
        engine = create_engine(database, **kwargs)
        with engine.connect() as con:
            df.to_sql(name, con=con, if_exists=if_exists, index=False)
