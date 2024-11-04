from typing import List, Dict, Optional
from wisecon.utils import time2int
from wisecon.types.request_data import BaseRequestData


__all__ = [
    "APICListRequestData",
    "APIStockFFlowDayLineRequestData",
    "APIUListNPRequestData",
    "APIDataV1RequestData",
    "APIStockKline",
    "APIStockKlineWithSSE",
    "APIMainHolder",
    "APIAnalystInvest",
    "APIMainHolderDetail",
    "APIStockTrends2",
]


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
    """"""
    def base_url(self) -> str:
        """"""
        return "https://push2his.eastmoney.com/api/qt/stock/kline/get"

    def base_sse(self) -> str:
        """"""
        return "https://push2his.eastmoney.com/api/qt/stock/kline/sse"

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


# todo: 封装请求数据类
