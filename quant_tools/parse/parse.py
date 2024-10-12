import re
import ast
from typing import Dict, List, Union, Tuple


__all__ = [
    "ParseBase",
]


class ParseBase:
    """"""
    matches: List[str] = None
    sparse_error: List[Tuple] = []

    @classmethod
    def greedy_mark(
            cls,
            string: str,
            mark_pattern: str,
    ) -> Union[List[List], List[Dict]]:
        """
        解析 value 贪婪模式，寻找第一个 'mark' 到最后一个 'mark' 之间的内容，适用于文本中只有 1 个 mark content 的解析。
        :param mark_pattern:
        :param string:
        :return:
        """
        cls.matches = re.findall(mark_pattern, string, flags=re.DOTALL)
        values = []
        for match in cls.matches:
            try:
                value = ast.literal_eval(match)
                values.append(value)
            except ValueError() as error:
                cls.sparse_error.append((match, f"Error: {error}"))
        return values

    @classmethod
    def eval_mark(
            cls,
            string: str,
            mark_pattern: str,
    ) -> Union[List[List], List[Dict]]:
        """
        解析 value 非贪婪模式，寻找任意 'mark' 之间 'mark' 之间的内容，适用于存在多个非嵌套模 value 的解析。
        :param mark_pattern:
        :param string:
        :return:

        example:
        """
        cls.matches = re.findall(mark_pattern, string, flags=re.DOTALL)
        values = []
        for match in cls.matches:
            try:
                value = ast.literal_eval(match)
                values.append(value)
            except ValueError() as error:
                cls.sparse_error.append((match, f"Error: {error}"))
        return values

    @classmethod
    def nested_data(
            cls,
            string: str,
            mark: tuple = ("{", "}"),
    ) -> Union[List[List], List[Dict]]:
        """
        解析嵌套的 values，基本适用于全部情况的 value 解析。
        :param mark:
        :param string:
        :return:

        example:
        """
        stack = []
        nested_values_idx = []

        for i, char in enumerate(string):
            if char == mark[0]:
                stack.append(i)
            elif char == mark[1]:
                if stack:
                    left_bracket_index = stack.pop()
                    if len(stack) == 0:
                        nested_values_idx.append((left_bracket_index, i + 1))

        nested_values = []
        for (start, end) in nested_values_idx:
            try:
                value = ast.literal_eval(string[start: end])
                nested_values.append(value)
            except ValueError() as error:
                cls.sparse_error.append((string[start: end], f"Error: {error}"))
        return nested_values
