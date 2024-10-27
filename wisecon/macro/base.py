from typing import Dict, Optional, List
from wisecon.types import APIDataV1RequestData
from wisecon.utils import time2int


__all__ = [
    "MacroRequestData"
]


class MacroRequestData(APIDataV1RequestData):
    """"""
    def base_param(self, update: Dict) -> Dict:
        """"""
        params = {
            "pageNumber": "1",
            "source": "WEB",
            "client": "WEB",
            "_": time2int(),
        }
        params.update(update)
        return params
