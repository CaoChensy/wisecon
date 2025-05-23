import re
import time
import click
from pydantic import Field
from fastmcp import FastMCP
from mcp.server.session import ServerSession
from typing import Dict, Union, Literal, Annotated
from wisecon.stock.kline import KLine
from wisecon.mcp.validate import *
from wisecon.stock.index import SearchKeyword, ConceptionMap, ListConceptionStock
from wisecon.backtrader.evaluate import PriceIndexEvaluator
from wisecon.stock.financial import StockBalance, StockIncome, StockCashFlow
from wisecon.stock.capital_flow import PlateFlow
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
def get_tool_version() -> str:
    """获取当前工具的版本号"""
    from wisecon import __version__
    return __version__


@mcp.tool()
def get_now_date():
    """获取当前日期"""
    return time.strftime("%Y-%m-%d", time.localtime())


@mcp.tool()
def search_keyword(
        keyword: Annotated[str, Field(description="keyword")],
):
    """根据关键词搜索行业、概念、地区、指数、基金、股票代码；关键词可以是名称、代码、简称、拼音等。

    搜索仅返回5条信息，如需更多结果，请使用其他接口。如：
        1. 使用`list_stock`可以获取所有行业、地区、概念板块下的股票列表；
    """
    keyword = re.sub("概念|行业|板块|指数|地域|基金|股票|代码", "", keyword)
    data = SearchKeyword(keyword=keyword).load()
    columns = [
        "code", "shortName", "securityTypeName", "market",
    ]
    return validate_response_data(data.to_frame()[columns])


@mcp.tool()
def analysis_stock_revenue(
        security_code: Annotated[str, Field(description="股票代码")],
        benchmark: Annotated[str, Field(description="基准指数，如：000300")] = "000300",
        size: Annotated[int, Field(description="数据条数", ge=1, le=1000)] = 252,
        risk_free_rate: Annotated[float, Field(description="无风险利率", ge=0, le=0.1)] = 0.03,
) -> Dict:
    """分析股票在一段时间中的收益"""
    df_300 = KLine(market_code=benchmark, period="1D", size=size).load().to_frame()
    df_stock = KLine(security_code=security_code, period="1D", size=size).load().to_frame()
    prices = df_stock[["time", "close"]].rename(columns={"close": "prices"})
    benchmark = df_300[["time", "close"]].rename(columns={"close": "benchmark"})
    df_data = prices.merge(benchmark, on="time", how="inner")
    df_data.prices = df_data.prices.astype(float)
    df_data.benchmark = df_data.benchmark.astype(float)
    evaluator = PriceIndexEvaluator(
        prices=df_data.prices, benchmark=df_data.benchmark,
        risk_free_rate=risk_free_rate, ols_alpha=True)
    return evaluator.evaluate()


@click.command()
@click.option("--host", "-p", default="127.0.0.1", type=str, required=False, help="host")
@click.option("--port", "-p", default=8000, type=int, required=False, help="port")
@click.option("--transport", "-p", default="stdio", type=str, required=False, help="transport")
def stock_analysis_mcp_server(
        host: str = None,
        port: Union[int, str] = None,
        transport: Literal["stdio", "sse"] = "stdio",
) -> None:
    """"""
    if transport == "sse":
        mcp.run(transport=transport, port=port, host=host)
    else:
        mcp.run(transport=transport)


if __name__ == "__main__":
    mcp.run(transport="sse", port=8005)
