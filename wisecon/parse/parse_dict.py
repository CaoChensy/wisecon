import re
from typing import List, Dict, Tuple
from .parse import ParseBase


__all__ = ['ParseDict']


class ParseDict(ParseBase):
    """"""
    matches: List[str] = None
    pattern: str = r'\{.*?\}'
    greedy_pattern: str = r'\{.*\}'
    # key_val_pattern = r"'([^']+)': '([^']*)'"
    key_val_pattern = r"['\"](\w+)['\"]:\s*['\"]([^'\"]+)['\"]"
    mark: Tuple[str] = ("{", "}")

    @classmethod
    def greedy_dict(cls, string: str, ) -> List[dict]:
        """
        解析dict贪婪模式，寻找第一个 '{' 到最后一个 '}' 之间的内容，适用于文本中只有 1 个字典的解析。
        :param string:
        :return:
        """
        return cls.greedy_mark(string=string, mark_pattern=cls.greedy_pattern)

    @classmethod
    def eval_dict(cls, string: str) -> List[Dict]:
        """
        解析dict非贪婪模式，寻找任意 '{' 之间 '}' 之间的内容，适用于存在多个非嵌套模型字典的解析。
        :param string:
        :return:

        example:

        """
        return cls.eval_mark(string=string, mark_pattern=cls.pattern)

    @classmethod
    def nested_dict(cls, string: str) -> List[Dict]:
        """
        解析嵌套的 dict，基本适用于全部情况的字典解析。
        :param string:
        :return:

        example:

        """
        return cls.nested_data(string=string, mark=cls.mark)

    @classmethod
    def key_value_dict(cls, string: str) -> List[Dict]:
        """
        todo: 还需要考虑单引号、双引号、还有多行识别未解决，有点麻烦
        依据冒号对 key-value 提取。
        :param string:
        :return:
        """
        tuple_data = re.findall(cls.key_val_pattern, string)
        return [dict(tuple_data)]
