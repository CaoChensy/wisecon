from pydantic import Field
from typing import Any, Dict, Callable, Optional
from quant_tools.types import BaseRequestConfig, ResponseData, BaseRequestData


__all__ = [
    "GovIncomeQueryConfig",
    "GovIncome",
]


class GovIncomeQueryConfig(BaseRequestConfig):
    """"""
    size: Optional[int] = Field(default=20)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_params(self) -> Dict:
        """
        :return:
        """
        columns = [
            "REPORT_DATE", "TIME", "BASE", "BASE_SAME", "BASE_SEQUENTIAL", "BASE_ACCUMULATE", "ACCUMULATE_SAME"
        ]
        params = {
            "columns": ",".join(columns),
            "pageNumber": "1",
            "pageSize": self.size,
            "sortColumns": "REPORT_DATE",
            "sortTypes": "-1",
            "source": "WEB",
            "client": "WEB",
            "reportName": "RPT_ECONOMY_INCOME",
            "_": self._current_time(),
        }
        return params


class GovIncome(BaseRequestData):
    """"""
    def __init__(
            self,
            query_config: Optional[GovIncomeQueryConfig] = None,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        if query_config is None:
            self.query_config = GovIncomeQueryConfig.model_validate(kwargs)
        else:
            self.query_config = query_config
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs

    def _base_url(self) -> str:
        """"""
        base_url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
        return base_url

    def load_data(self) -> ResponseData:
        """
        :return:
        """
        metadata = self.request_json().get("result", {})
        data = metadata.pop("data")
        self.update_metadata(metadata)
        self._logger(msg=f"[{__class__.__name__}] Find {len(data)} reports.", color="green")
        return ResponseData(data=data, metadata=metadata)

    def update_metadata(self, metadata: Dict):
        """"""
        metadata.update({
            "description": "中国 财政收入（每年2月公布当年1-2月累计值）",
            "columns": {
                "START_DATE": "开始时间",
                "END_DATE": "截至时间",
                "BASE": "当月(亿元)",
                "BASE_SAME": "同比增长",
                "BASE_SEQUENTIAL": "环比增长",
                "BASE_ACCUMULATE": "累计(亿元)",
                "ACCUMULATE_SAME": "累计同比增长",
            }
        })