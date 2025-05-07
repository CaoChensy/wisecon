import click
from pydantic import Field
from fastmcp import FastMCP
from typing import Union, Literal
from wisecon.stock.kline import KLine
from wisecon.mcp.validate import *


mcp = FastMCP("Wisecon MCP")


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
