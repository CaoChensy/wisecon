import pprint
import pandas as pd
from pydantic import BaseModel, Field
from typing import Any, List, Dict, Literal, Optional


__all__ = [
    "Metadata",
    "ResponseData",
]


class Metadata(BaseModel):
    """"""
    columns: Dict[str, Any] = Field(default={})
    description: str = Field(default="")
    response: Dict[str, Any] = Field(default={})

    def __init__(self, **kwargs: Any):
        """元数据

        Args:
            **kwargs: 参数
        """
        super().__init__(**kwargs)
        self.columns = {k: v for k, v in self.columns.items() if v}


class ResponseData(BaseModel):
    """请求返回数据的数据类"""
    metadata: Optional[Metadata] = Field(default=None)
    data: List[Dict] = Field(default=[])

    def __init__(
            self,
            data: List[Dict],
            metadata: Optional[Metadata] = None,
            **kwargs: Any,
    ):
        """封装请求返回数据方法类

        Args:
            data: 返回数据
            metadata: 元数据
            **kwargs: 其他参数
        """
        super().__init__(**kwargs)
        self.data = data
        self.metadata = metadata

    def show_columns(self):
        """展示数据的字段信息"""
        pprint.pprint(self.metadata.columns, indent=4)

    def _trans_chinese_columns(self, item: Dict) -> Dict:
        """将数据转换为中文名

        Args:
            item: 一条数据

        Returns:
            Dict: 转换后的数据
        """
        return {self.metadata.columns.get(key, key): value for key, value in item.items()}

    def drop_no_zh_columns(self):
        """删除非中文字段"""
        exits_columns = [k for k, v in self.metadata.columns.items() if v]
        self.data = [{k: v for k, v in item.items() if k in exits_columns} for item in self.data]

    def to_dict(
            self,
            chinese_column: Optional[bool] = False,
    ) -> List[Dict]:
        """
        Args:
            chinese_column: 是否将列名翻译为中文

        Returns:
            List[Dict]: 转换后的数据
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
        """返回数据的 pandas.DataFrame

        Args:
            chinese_column: 是否将列名翻译为中文

        Returns:
            dataframe: 数据的 pandas.DataFrame
        """
        df = pd.DataFrame(data=self.data)
        if chinese_column:
            df.rename(columns=self.metadata.columns, inplace=True)
        return df

    def to_markdown(
            self,
            chinese_column: Optional[bool] = False,
            **kwargs: Any,
    ) -> str:
        """返回 Markdown 格式的数据

        Args:
            chinese_column: 是否将列名翻译为中文
            **kwargs: to_markdown() 的参数

        Returns:
            str: markdown 格式的数据
        """
        return self.to_frame(chinese_column).to_markdown(**kwargs)

    def to_csv(
            self,
            path: str,
            chinese_column: Optional[bool] = False,
            **kwargs: Any
    ) -> None:
        """将数据保存至 csv 文件中

        Args:
            path: csv 文件路径
            chinese_column: 是否将列名翻译为中文
            **kwargs: 其他参数
        """
        self.to_frame(chinese_column).to_csv(path, **kwargs)

    def to_excel(
            self,
            path: str,
            chinese_column: Optional[bool] = False,
            **kwargs: Any
    ) -> None:
        """将数据保存至 excel 文件中

        Args:
            path: excel 文件路径
            chinese_column: 是否将列名翻译为中文
            **kwargs: 其他参数
        """
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
        """将数据存储为 parquet 文件

        Args:
            path: 文件路径
            chinese_column: 是否使用中文列名
            index: 是否包含索引
            engine: 存储引擎
            compression: 压缩格式
            **kwargs: 其他参数
        """
        self.to_frame(chinese_column).to_parquet(
            path, index=index, engine=engine,
            compression=compression, **kwargs)

    def to_pickle(
            self,
            path: str,
            chinese_column: Optional[bool] = False,
            **kwargs: Any,
    ):
        """将数据存储为 pickle 文件

        Args:
            path: 文件保存路径
            chinese_column: 是否使用中文列名
            **kwargs: 其他参数
        """
        self.to_frame(chinese_column).to_pickle(path,  **kwargs)

    def to_string(
            self,
            chinese_column: Optional[bool] = False,
            **kwargs: Any
    ) -> str:
        """将数据转换为 string 格式

        Args:
            chinese_column: 是否将列名转换为中文
            **kwargs: 其他参数

        Returns:
            str: 数据的 string 格式
        """
        return self.to_frame(chinese_column).to_string(**kwargs)

    def to_sql(
            self,
            name: str,
            con: Any,
            chinese_column: Optional[bool] = False,
            if_exists: Literal["fail", "replace", "append"] = "fail",
            index: Optional[bool] = True,
            **kwargs: Any,
    ):
        """将数据存储至 Database 中

        Args:
            name: 表名
            con: 数据库连接
            chinese_column: 是否将列名转为中文
            if_exists: 如果表已存在，则采取的操作
            index: 是否将索引存储至数据库中
            **kwargs: 其他参数
        """
        self.to_frame(chinese_column).to_sql(
            name=name, con=con, if_exists=if_exists,
            index=index, **kwargs)

    def to_duckdb(
            self,
            database: str,
            name: str,
            chinese_column: Optional[bool] = False,
            if_exists: Literal["fail", "replace", "append"] = "replace",
            **kwargs: Any,
    ):
        """将数据存储至 duckdb 数据库中

        Args:
            database: 数据库文件路径
            name: 表名
            chinese_column: 是否将列名转为中文
            if_exists: 如果表存在，是否覆盖
            **kwargs: 其他参数
        """
        from sqlalchemy import create_engine

        df = self.to_frame(chinese_column)
        engine = create_engine(database, **kwargs)
        with engine.connect() as con:
            df.to_sql(name, con=con, if_exists=if_exists, index=False)
