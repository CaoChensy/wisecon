import pprint
import pandas as pd
from pydantic import BaseModel, Field
from typing import List, Dict, Union, Optional


__all__ = [
    "ResponseData",
]


class ResponseData(BaseModel):
    """"""
    metadata: Optional[Dict] = Field(default={})
    data: List[Dict] = Field(default=[])

    def __init__(
            self,
            data: List[Dict],
            metadata: Optional[Dict] = None,
            **kwargs
    ):
        """"""
        super().__init__(**kwargs)
        self.data = data
        self.metadata = metadata

    def pprint_metadata(self):
        """"""
        pprint.pprint(self.metadata, indent=4)

    def to_dict(self) -> List[Dict]:
        """"""
        return self.data

    def to_frame(self, columns: Optional[Union[List, List[Dict]]] = None) -> pd.DataFrame:
        """"""
        df = pd.DataFrame(data=self.data)
        if columns and isinstance(columns, dict):
            df.rename(columns=columns, inplace=True)
        elif columns and isinstance(columns, list):
            df.columns = columns
        return df
