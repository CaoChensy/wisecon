import time
from datetime import datetime
from typing import Tuple, Literal


__all__ = [
    "time2int",
    "year2date",
]


def time2int() -> str:
    """将当前时间转换为毫秒级时间戳

    Returns:
        毫秒级时间戳
    """
    return str(int(time.time() * 1E3))


def year2date(
        year: int,
        format: Literal["%Y%m%d", "%Y-%m-%d"] = "%Y%m%d"
) -> Tuple[str, str]:
    """给定一个年份，返回该年份的开始与结束日期

    Args:
        year: 年份
        format: 日期格式

    Returns:
        start_date: 开始日期
        end_date: 结束日期
    """
    start_date = datetime(year, 1, 1).strftime(format)
    end_date = datetime(year, 12, 31).strftime(format)
    return start_date, end_date
