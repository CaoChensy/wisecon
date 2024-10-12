import re
from typing import List, Dict, Tuple
from .parse import ParseBase


__all__ = ["ParseList"]


class ParseList(ParseBase):
    """"""
    matches: List[str] = None
    pattern: str = r'\[.*?\]'
    greedy_pattern: str = r'\[.*\]'
    mark: Tuple[str] = ("[", "]")

    @classmethod
    def greedy_list(cls, string: str) -> List[List]:
        """"""
        return cls.greedy_mark(string=string, mark_pattern=cls.greedy_pattern)

    @classmethod
    def eval_list(cls, string: str) -> List[List]:
        """"""
        return cls.eval_mark(string=string, mark_pattern=cls.pattern)

    @classmethod
    def nested_list(cls, string: str) -> List[List]:
        """"""
        return cls.nested_data(string=string, mark=cls.mark)

