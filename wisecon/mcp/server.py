import click
import pandas as pd
from pydantic import Field
from fastmcp import FastMCP
from typing import Union, Literal, Optional
from wisecon.stock.kline import KLine


mcp = FastMCP("Wisecon MCP")


def validate_response_data(data: Union[list, pd.DataFrame]) -> str:
    """"""
    if len(data) == 0:
        return "No data found."
    prefix = ""
    if len(data) > 50:
        prefix = "Data too large, showing first 50 rows:\n\n"

    if isinstance(data, list):
        data = str(data[:50])
    elif isinstance(data, pd.DataFrame):
        data = data.head(50).to_markdown(index=False)
    data = f"{prefix}{data}"
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
    return response.to_markdown()


@click.command()
@click.option("--port", "-p", default=8000, type=int, required=False, help="port")
@click.option("--transport", "-p", default="stdio", type=str, required=False, help="transport")
def wisecon_mcp_server(
        transport: Literal["stdio", "sse"] = "stdio",
        port: Union[int, str] = None,
) -> None:
    """"""
    if transport == "sse":
        mcp.run(transport=transport, port=port)
    else:
        mcp.run(transport=transport)
