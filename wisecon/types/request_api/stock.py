import json
import requests
from urllib.parse import quote
from datetime import datetime
from typing import List, Dict, Optional
from requests import Response
from wisecon.utils import time2int
from wisecon.types import ResponseData, assemble_url
from wisecon.types.request_data import BaseRequestData
from lumix.structured import ParseDict


__all__ = [
    "APISearch",
    "APIConceptionBK",
    "APICListRequestData",
    "APIStockFFlowKLineRequestData",
    "APIStockFFlowDayLineRequestData",
    "APIUListNPRequestData",
    "APIDataRequestData",
    "APIDataV1RequestData",
    "APIStockKline",
    "APIStockKlineWithSSE",
    "APIMainHolder",
    "APIAnalystInvest",
    "APIMainHolderDetail",
    "APIStockTrends2",
    "APIMarketSummary",
    "APIAnnouncement",
    "APIAskSecretary",
]


class APISearch(BaseRequestData):
    """"""
    def base_url(self) -> str:
        return "https://search-codetable.eastmoney.com/codetable/search/web"

    def base_param(self, update: Dict) -> Dict:
        """"""
        params = {
            "client": "web",
            "clientType": "webSuggest",
            "clientVersion": "lastest",
            "pageIndex": 1,
            "pageSize": 5,
        }
        params.update(update)
        return params

    def clean_json(
            self,
            json_data: Optional[Dict],
    ) -> List[Dict]:
        """"""
        response = json_data
        data = response.pop("result")
        self.metadata.response = response
        return data


class APIConceptionBK(BaseRequestData):
    """"""
    def base_url(self) -> str:
        """"""
        return "https://reportapi.eastmoney.com/report/bk"


class APICListRequestData(BaseRequestData):
    """"""
    def base_url(self) -> str:
        return "https://push2.eastmoney.com/api/qt/clist/get"

    def base_param(self, update: Dict) -> Dict:
        """"""
        params = {
            "pn": 1,
            "po": 1,
            "np": 1,
            "fltt": 2,
            "invt": 2,
            "dect": 1,
            "wbp2u": "|0|0|0|web",
            "_": time2int(),
        }
        params.update(update)
        return params

    def clean_json(
            self,
            json_data: Optional[Dict],
    ) -> List[Dict]:
        """"""
        response = json_data.get("data", {})
        data = response.pop("diff")
        self.metadata.response = response
        return data

    def load(self) -> ResponseData:
        """"""
        data = []
        params = self.params()
        json_data = self.load_response_json(params=params)
        batch_data = self.clean_json(json_data)
        data.extend(batch_data)
        while len(data) < self.metadata.response.get("total"):
            params["pn"] = params["pn"] + 1
            json_data = self.load_response_json(params)
            batch_data = self.clean_json(json_data)
            data.extend(batch_data)
        return ResponseData(data=data, metadata=self.metadata)


class APIStockFFlowKLineRequestData(BaseRequestData):
    """"""
    def base_url(self) -> str:
        return "https://push2.eastmoney.com/api/qt/stock/fflow/kline/get"

    def base_param(self, update: Dict) -> Dict:
        """"""
        params = {
            "_": time2int(),
        }
        params.update(update)
        return params

    def clean_json(
            self,
            json_data: Optional[Dict],
    ) -> List[Dict]:
        """"""
        columns = list(self.mapping.columns.keys())
        response = json_data.get("data", {})
        data = response.pop("klines")
        data = [dict(zip(columns, item.split(","))) for item in data]
        self.metadata.response = response
        return data


class APIStockFFlowDayLineRequestData(BaseRequestData):
    """"""
    def base_url(self) -> str:
        return "https://push2his.eastmoney.com/api/qt/stock/fflow/daykline/get"

    def clean_json(
            self,
            json_data: Optional[Dict],
    ) -> List[Dict]:
        """"""
        columns = list(self.mapping.columns.keys())
        response = json_data.get("data", {})
        data = response.pop("klines")
        data = [dict(zip(columns, item.split(","))) for item in data]
        self.metadata.response = response
        return data


class APIUListNPRequestData(BaseRequestData):
    """"""
    def base_url(self) -> str:
        return "https://push2.eastmoney.com/api/qt/ulist.np/get"

    def clean_json(
            self,
            json_data: Optional[Dict],
    ) -> List[Dict]:
        """"""
        response = json_data.get("data", {})
        data = response.pop("diff")
        self.metadata.response = response
        return data


class APIDataRequestData(BaseRequestData):
    """"""
    conditions: Optional[List[str]]
    security_code: Optional[str]
    start_date: Optional[str]
    end_date: Optional[str]
    date: Optional[str]

    def base_url(self) -> str:
        """"""
        return "https://datacenter-web.eastmoney.com/api/data/get"

    def clean_json(
            self,
            json_data: Optional[Dict],
    ) -> List[Dict]:
        """"""
        response = json_data.get("result", {})
        try:
            data = response.pop("data")
            self.metadata.response = response
            return data
        except Exception as e:
            raise ValueError(f"Error in cleaning json data; response: {json_data}")

    def filter_report_date(self, date_name: Optional[str] = "REPORT_DATE"):
        """"""
        if hasattr(self, "start_date") and self.start_date:
            self.conditions.append(f"({date_name}>='{self.start_date}')")
        if hasattr(self, "end_date") and self.end_date:
            self.conditions.append(f"({date_name}<='{self.end_date}')")
        if hasattr(self, "date") and self.date:
            self.conditions.append(f"({date_name}='{self.date}')")

    def filter_security_code(self):
        """"""
        if self.security_code:
            self.conditions.append(f'(SECURITY_CODE="{self.security_code}")')

    def base_param(self, update: Dict) -> Dict:
        """"""
        params = {
            "extraCols": "",
            "filter": "",
            "sr": "",
            "st": "",
            "token": "",
            "var": "",
            "source": "QuoteWeb",
            "client": "WEB",
            "_": time2int(),
        }
        params.update(update)
        return params


class APIDataV1RequestData(BaseRequestData):
    """"""
    conditions: Optional[List[str]]
    security_code: Optional[str]
    start_date: Optional[str]
    end_date: Optional[str]
    date: Optional[str]

    def base_url(self) -> str:
        """"""
        return "https://datacenter-web.eastmoney.com/api/data/v1/get"

    def clean_json(
            self,
            json_data: Optional[Dict],
    ) -> List[Dict]:
        """"""
        response = json_data.get("result", {})
        try:
            data = response.pop("data")
            self.metadata.response = response
            return data
        except Exception as e:
            raise ValueError(f"Error in cleaning json data; response: {json_data}")

    def filter_report_date(self, date_name: Optional[str] = "REPORT_DATE"):
        """"""
        if hasattr(self, "start_date") and self.start_date:
            self.conditions.append(f"({date_name}>='{self.start_date}')")
        if hasattr(self, "end_date") and self.end_date:
            self.conditions.append(f"({date_name}<='{self.end_date}')")
        if hasattr(self, "date") and self.date:
            self.conditions.append(f"({date_name}='{self.date}')")

    def filter_security_code(self):
        """"""
        if self.security_code:
            self.conditions.append(f'(SECURITY_CODE="{self.security_code}")')

    def base_param(self, update: Dict) -> Dict:
        """"""
        params = {
            "columns": "ALL",
            "pageNumber": "1",
            "quoteColumns": "",
            "source": "WEB",
            "client": "WEB",
            "_": time2int(),
        }
        params.update(update)
        return params


class APIStockKline(BaseRequestData):
    """"""
    def base_url(self) -> str:
        """"""
        return "https://push2his.eastmoney.com/api/qt/stock/kline/get"

    def clean_json(
            self,
            json_data: Optional[Dict],
    ) -> List[Dict]:
        response = json_data.get("data", {})
        data = response.pop("klines")
        self.metadata.response = response

        def trans_kline_data(line: str) -> Dict:
            """"""
            line_data = line.split(",")
            return dict(zip(list(self.mapping.columns.keys()), line_data))

        data = list(map(trans_kline_data, data))
        return data


class APIStockKlineWithSSE(BaseRequestData):
    """
    URL - 1
        https://push2his.eastmoney.com/api/qt/stock/kline/get
        https://push2his.eastmoney.com/api/qt/stock/kline/sse

    URL - 2
        https://push2.eastmoney.com/api/qt/stock/get
        https://push2.eastmoney.com/api/qt/stock/sse
    """
    def base_url(self) -> str:
        """"""
        return "https://push2.eastmoney.com/api/qt/stock/get"

    def base_sse(self) -> str:
        """"""
        return "https://push2.eastmoney.com/api/qt/stock/sse"

    def clean_json(
            self,
            json_data: Optional[Dict],
    ) -> List[Dict]:
        """"""

        def clean_data(data: Dict) -> Dict:
            """"""
            columns = [
                "f11", "f13", "f15", "f17", "f19",
                "f31", "f33", "f35", "f37", "f39",
                "f191",
            ]
            for key, value in data.items():
                if key in columns:
                    data.update({key: value / 100})
            return data

        data = list(map(clean_data, [json_data.pop("data")]))
        self.metadata.response = json_data
        return data


class APIMainHolder(BaseRequestData):
    """"""
    def base_url(self) -> str:
        """"""
        return "https://data.eastmoney.com/dataapi/zlsj/list"

    def base_param(self, update: Dict) -> Dict:
        """"""
        params = {
            "sortDirec": "1",
            "pageNum": "1",
        }
        params.update(update)
        return params

    def clean_json(
            self,
            json_data: Optional[Dict],
    ) -> List[Dict]:
        """"""
        data = json_data.pop("data", {})
        self.metadata.response = json_data
        return data


class APIAnalystInvest(BaseRequestData):
    """"""
    def base_url(self) -> str:
        """"""
        return "https://data.eastmoney.com/dataapi/invest/list"

    def base_param(self, update: Dict) -> Dict:
        """"""
        params = {
            "columns": "ALL",
            "source": "WEB",
            "client": "WEB",
            "pageNumber": "1",
        }
        params.update(update)
        return params

    def clean_json(
            self,
            json_data: Optional[Dict],
    ) -> List[Dict]:
        """"""
        response = json_data.pop("result", {})
        data = response.pop("data", [])
        self.metadata.response = response
        return data


class APIMainHolderDetail(BaseRequestData):
    """"""
    def base_url(self) -> str:
        """"""
        return "https://data.eastmoney.com/dataapi/zlsj/detail"

    def base_param(self, update: Dict) -> Dict:
        """"""
        params = {
            "SHCode": "",
            "sortDirec": "1",
            "pageNum": "1",
        }
        params.update(update)
        return params

    def clean_json(
            self,
            json_data: Optional[Dict],
    ) -> List[Dict]:
        """"""
        data = json_data.pop("data", {})
        self.metadata.response = json_data
        return data


class APIStockTrends2(BaseRequestData):
    """"""
    def base_url(self) -> str:
        """"""
        return "https://push2his.eastmoney.com/api/qt/stock/trends2/get"

    def base_param(self, update: Dict) -> Dict:
        """"""
        params = {
            "fields1": "f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13,f17",
            "fields2": "f51,f52,f53,f54,f55,f56,f57,f58",
            "mpi": "1000",
            "iscr": "0",
            "iscca": "0",
            "wbp2u": "|0|0|0|web",
        }
        params.update(update)
        return params

    def clean_json(
            self,
            json_data: Optional[Dict],
    ) -> List[Dict]:
        """
        Args:
            json_data:

        Returns:


            response = json_data.get("data", {})
            data = response.pop("klines")
            data = [dict(zip(columns, item.split(","))) for item in data]
            self.metadata.response = response
        """
        columns = list(self.mapping.columns.keys())
        response = json_data.pop("data", {})
        data = response.pop("trends", [])
        data = [dict(zip(columns, item.split(","))) for item in data]
        self.metadata.response = response
        return data


class APIMarketSummary(BaseRequestData):
    """"""
    def base_url(self) -> str:
        """"""
        return "https://quote.eastmoney.com/newapi/sczm"

    def base_param(self, update: Dict) -> Dict:
        """"""
        params = {}
        params.update(update)
        return params

    def clean_json(
            self,
            json_data: Optional[Dict],
    ) -> List[Dict]:
        """"""
        data_name = ["ss", "cyb", "hs"]
        data = [json_data.pop(d_name) for d_name in data_name]
        self.metadata.response = json_data
        return data


class APIAskSecretary(BaseRequestData):
    """"""
    def base_url(self) -> str:
        """"""
        return "https://search-api-web.eastmoney.com/search/jsonp"

    def base_param(self, update: Dict) -> Dict:
        """"""
        params = {}
        params.update(update)
        return params

    def clean_content(
            self,
            content: Optional[str],
    ) -> List[Dict]:
        """"""
        response = ParseDict.greedy_dict(content)[0]
        result_data = response.pop("result")
        data = result_data.pop("wenDongMiWeb", [])
        self.metadata.response = response
        return data

    def request(self, params: Optional[Dict] = None) -> Response:
        """"""
        base_url = self.base_url()
        if params is None:
            params = self.params()
        url = assemble_url(base_url, params)
        self._logger(msg=f"[URL] {url}\n", color="green")
        response = requests.get(url, headers=self.headers)
        return response

    def load(self) -> ResponseData:
        """"""
        data = []
        params = self.params()
        params["param"] = quote(json.dumps(params["param"], ensure_ascii=False, separators=(',', ':')))
        text_data = self.load_response_text(params=params)
        batch_data = self.clean_content(text_data)
        data.extend(batch_data)
        total = self.metadata.response.get("hitsTotal")
        while len(data) < total:
            _param = self.params()
            _param["param"]["param"]["wenDongMiWeb"]["pageindex"] += 1
            params["param"] = quote(json.dumps(_param["param"], ensure_ascii=False, separators=(',', ':')))
            text_data = self.load_response_text(params=params)
            batch_data = self.clean_content(text_data)
            data.extend(batch_data)
        return ResponseData(data=data, metadata=self.metadata)


class APIAnnouncement(BaseRequestData):
    """"""
    date: str

    def base_url(self) -> str:
        """"""
        return "https://np-anotice-stock.eastmoney.com/api/security/ann"

    def base_param(self, update: Dict) -> Dict:
        """"""
        params = {
            "sr": "-1",
            "page_size": 50,
            "page_index": 1,
            "client_source": "web",
            "s_node": "0",
        }
        params.update(update)
        return params

    def clean_json(
            self,
            json_data: Optional[Dict],
    ):
        """"""
        response = json_data.get("data", {})
        data = response.get("list", [])
        self.metadata.response = response
        return data

    def load(self) -> ResponseData:
        """"""
        params = self.params()
        json_data = self.load_response_json(params=params)
        batch_data = self.clean_json(json_data)
        date_data = [
            item for item in batch_data
            if datetime.strptime(item.get("notice_date").split(" ")[0], "%Y-%m-%d")\
               >= datetime.strptime(self.date, "%Y-%m-%d")]
        if len(batch_data) > len(date_data):
            return ResponseData(data=date_data, metadata=self.metadata)
        else:
            while True:
                params["page_index"] += 1
                json_data = self.load_response_json(params=params)
                batch_data = self.clean_json(json_data)
                _date_data = [
                    item for item in batch_data
                    if datetime.strptime(item.get("notice_date").split(" ")[0], "%Y-%m-%d")\
                       >= datetime.strptime(self.date, "%Y-%m-%d")]
                date_data.extend(_date_data)
                if len(batch_data) > len(_date_data):
                    return ResponseData(data=date_data, metadata=self.metadata)
