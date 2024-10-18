import time
from datetime import datetime
from typing import Tuple, Literal


__all__ = [
    "time2int",
    "year2date",
]


def time2int() -> str:
    """"""
    return str(int(time.time() * 1E3))


def year2date(
        year: int,
        format: Literal["%Y%m%d", "%Y-%m-%d"] = "%Y%m%d"
) -> Tuple[str, str]:
    """"""
    start_date = datetime(year, 1, 1).strftime(format)
    end_date = datetime(year, 12, 31).strftime(format)
    return start_date, end_date
