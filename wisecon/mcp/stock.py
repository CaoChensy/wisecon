import click
import time
from pydantic import Field
from fastmcp import FastMCP
from mcp.server.session import ServerSession
from typing import Union, Literal, Annotated
from wisecon.stock.kline import KLine
from wisecon.mcp.validate import *
from wisecon.stock.index import SearchKeyword, ConceptionMap
from wisecon.stock.financial import StockBalance, StockIncome, StockCashFlow
from wisecon.utils.time import is_quarter_end


####################################################################################
# Temporary monkeypatch which avoids crashing when a POST message is received
# before a connection has been initialized, e.g: after a deployment.
# pylint: disable-next=protected-access
old__received_request = ServerSession._received_request


async def _received_request(self, *args, **kwargs):
    try:
        return await old__received_request(self, *args, **kwargs)
    except RuntimeError:
        pass


# pylint: disable-next=protected-access
ServerSession._received_request = _received_request
####################################################################################


mcp = FastMCP("Wisecon MCP")


@mcp.tool()
def get_now_date():
    """获取当前日期"""
    return time.strftime("%Y-%m-%d", time.localtime())


@mcp.tool()
def list_industry() -> dict:
    """获取行业列表"""
    con_map = ConceptionMap()
    df_industry = con_map.map_industry.to_frame()
    data = dict(zip(df_industry.bkCode, df_industry.bkName))
    return data


@mcp.tool()
def fetch_stock_data(
        security_code: str = Field(description="security code"),
        period: Literal["1m", "5m", "15m", "30m", "60m", "1D", "1W", "1M"] = Field(default="1D", description="data period"),
        size: int = Field(default=10, description="data size"),
):
    """"""
    data = KLine(security_code=security_code, period=period, size=size).load()
    response = data.to_frame(chinese_column=True)
    return validate_response_data(response)


@mcp.tool()
def search_keyword(
        keyword: Annotated[str, Field(description="keyword")],
):
    """搜索关键词，关键词可以是名称、代码、简称、拼音
    查询板块代码、行业代码、概念代码、地域代码、指数代码、基金代码、股票代码等信息"""
    data = SearchKeyword(keyword=keyword).load()
    columns = [
        "code", "shortName", "securityTypeName", "market",
    ]
    return validate_response_data(data.to_frame()[columns])


@mcp.tool()
def fetch_financial_sheet(
        sheet_type: Annotated[Literal["income", "balance", "cash"], Field(description="sheet type")],
        security_code: Annotated[str, Field(description="security code")] = None,
        industry_name: Annotated[str, Field(description="industry name")] = None,
        date: Annotated[str, Field(description="date")] = None,
        size: Annotated[int, Field(description="data size")] = 10
):
    """根据行业名称、股票代码获取财务报表
    1. 获取上市公司资产负债表、利润表、现金流表
    2. 获取某个行业下全部公司的资产负债表、利润表、现金流表

    Args:
        sheet_type: 资产负债表类型，可选:
            - "balance": 资产负债表
            - "income": 利润表
            - "cash": 现金流表
        security_code: 股票代码，一般为6位数字，如 "603889"
        industry_name: 行业名称，如 "纺织服装"
        date: 日期，必须是季度末，如 "2024-01-31"
        size: 数据大小，默认为10

    Returns: 财务报表数据
    """

    if not is_quarter_end(date):
        return "date must be a quarter end"

    if industry_name is not None:
        con_map = ConceptionMap()
        df_industry = con_map.map_industry.to_frame()
        if industry_name not in df_industry["bkName"].tolist():
            return "industry name not found"
    sheet_cls = {
        "balance": StockBalance,
        "income": StockIncome,
        "cash": StockCashFlow,
    }
    sheet = sheet_cls.get(sheet_type)(
        security_code=security_code, industry_name=industry_name, date=date, size=size
    )
    response = sheet.load()
    return validate_response_data(response.to_frame(chinese_column=True))


@click.command()
@click.option("--port", "-p", default=8000, type=int, required=False, help="port")
@click.option("--transport", "-p", default="stdio", type=str, required=False, help="transport")
def stock_mcp_server(
        transport: Literal["stdio", "sse"] = "stdio",
        port: Union[int, str] = None,
) -> None:
    """"""
    if transport == "sse":
        mcp.run(transport=transport, port=port)
    else:
        mcp.run(transport=transport)
