from typing import List, Dict, Optional
from wisecon.types.request_data import BaseRequestData


__all__ = [
    "APIMovieRequestData",
    "APITVRequestData",
]


class APIMovieRequestData(BaseRequestData):
    """"""
    def base_url(self) -> str:
        return "https://piaofang.maoyan.com/getBoxList"

    def base_param(self, update: Dict) -> Dict:
        """"""
        params = {"date": 1, "isSplit": "true"}
        params.update(update)
        return params

    def clean_json(
            self,
            json_data: Optional[Dict],
    ) -> List[Dict]:
        """"""
        tv_list = json_data.get("boxOffice", {})
        data = tv_list.pop("data")
        self.metadata.response = data.get("updateInfo")
        data_list = data.get("list")
        for item in data_list:
            movie_item = item.pop("movieInfo")
            item.update(movie_item)
        return data_list


class APITVRequestData(BaseRequestData):
    """"""
    def base_url(self) -> str:
        return "https://piaofang.maoyan.com/getTVList"

    def base_param(self, update: Dict) -> Dict:
        """"""
        params = {"showDate": 2}
        params.update(update)
        return params

    def clean_json(
            self,
            json_data: Optional[Dict],
    ) -> List[Dict]:
        """"""
        tv_list = json_data.get("tvList", {})
        data = tv_list.pop("data")
        self.metadata.response = data.get("updateInfo")
        return data.get("list")
