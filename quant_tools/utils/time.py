import time


__all__ = [
    "time2int",
]


def time2int() -> str:
    """"""
    return str(int(time.time() * 1E3))

