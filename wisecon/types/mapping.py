from typing import Dict
from pydantic import BaseModel


__all__ = [
    "BaseMapping",
    "APICListMapping",
]


class BaseMapping(BaseModel):
    """"""
    columns: Dict[str, str]

    def reverse(self, mapping_name: str) -> Dict:
        """"""
        if hasattr(self, mapping_name) and isinstance(getattr(self, mapping_name), dict):
            return {v: k for k, v in getattr(self, mapping_name).items()}
        else:
            raise ValueError(f"Mapping {mapping_name} not found in {self.__class__.__name__}")

    def filter_columns(self, columns: Dict) -> Dict:
        """"""
        return {k: v for k, v in columns.items() if v}


class APICListMapping(BaseMapping):
    """"""
    columns: Dict[str, str] = {
        "f12": "code",
        "f13": "prefix_code",
        "f14": "名称",
        "f62": "今日主力净流入(净额)"
    }
