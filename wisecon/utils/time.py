import time
from datetime import datetime
from typing import Tuple, Literal


__all__ = [
    "time2int",
    "year2date",
    "is_quarter_end",
    "get_quarter_ends",
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


def is_quarter_end(date: datetime | str | None = None) -> bool:
    """判断给定日期是否为季度的最后一天

    Args:
        date_input: 判断是否为季度的最后一天，支持以下输入格式：
            - None: 默认使用当前日期
            - datetime 对象
            - str 格式："yyyyMMdd" 或 "yyyy-MM-dd"

    Returns: bool
    """
    if date is None:
        date = datetime.today()
    elif isinstance(date, datetime):
        date = date
    elif isinstance(date, str):
        try:
            if '-' in date:
                date = datetime.strptime(date, "%Y-%m-%d")
            else:
                date = datetime.strptime(date, "%Y%m%d")
        except ValueError:
            raise ValueError("字符串格式错误，请使用 'yyyy-MM-dd' 或 'yyyyMMdd'")
    else:
        raise TypeError("不支持的数据类型，请传入 datetime 或 str")

    quarter_ends = {
        3: 31,
        6: 30,
        9: 30,
        12: 31,
    }
    return date.month in quarter_ends and date.day == quarter_ends[date.month]


def get_quarter_ends(start_date, end_date):
    """

    Args:
        start_date:
        end_date:

    Returns:

    """
    quarter_ends = []

    # 定义每个季度的最后一天
    quarter_end_days = {
        1: '03-31',
        2: '06-30',
        3: '09-30',
        4: '12-31'
    }

    start_year = int(start_date[:4])
    end_year = int(end_date[:4])

    for year in range(start_year, end_year + 1):
        for q in range(1, 5):
            month_day = quarter_end_days[q]
            q_end = f"{year}-{month_day}"
            if start_date <= q_end <= end_date:
                quarter_ends.append(q_end)

    return quarter_ends
