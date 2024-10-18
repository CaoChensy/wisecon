import time
import random


__all__ = [
    "headers",
    "Constant",
    "get_current_timestamp",
    "jquery_mock_callback",
]


headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
}


class Constant:
    jQuery_Version = "1.8.3"


def get_current_timestamp() -> int:
    return int(round(time.time() * 1000))


def jquery_mock_callback() -> str:
    return f'jQuery{(Constant.jQuery_Version + str(random.random())).replace(".", "")}_{str(get_current_timestamp() - 1000)}'
