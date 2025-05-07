from typing import Dict
from pydantic import BaseModel


__all__ = [
    "headers"
]


class Headers(BaseModel):
    """"""
    headers: Dict = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
    }


headers = Headers()

