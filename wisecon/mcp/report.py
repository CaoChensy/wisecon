import re
import time
import click
from pydantic import Field
from fastmcp import FastMCP
from typing import Union, Literal, Annotated
from wisecon.report import Report, ConceptionMap
from wisecon.mcp.validate import *
from mcp.server.session import ServerSession


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
def get_industry_name_by_code(code: Annotated[str, Field(description="行业代码")]) -> str:
    """根据行业代码获取行业名称"""
    con_map = ConceptionMap()
    return validate_response_data(con_map.get_name_by_code(code))


@mcp.tool()
def get_industry_code_by_name(keyword: Annotated[str, Field(description="行业名称关键词")]) -> str:
    """根据行业名称关键词进行模糊查询，获取与该关键词匹配的行业代码"""
    con_map = ConceptionMap()
    return validate_response_data(con_map.get_code_by_name(keyword))


@mcp.tool()
def list_industry() -> dict:
    """获取行业列表"""
    con_map = ConceptionMap()
    df_industry = con_map.map_industry.to_frame()
    data = dict(zip(df_industry.bkCode, df_industry.bkName))
    return data


@mcp.tool()
def list_report(
        report_type: Annotated[Literal["个股研报", "行业研报", "策略报告", "宏观研究", "券商晨报", "*"], Field(description="研报类型，'*' 为不限定研报类型")],
        code: Annotated[str, Field(description="股票代码, 如600000")] = None,
        industry_code: Annotated[Union[str, int], Field(description="行业代码(如 '451'), '*' 为不限定行业")] = "*",
        date: Annotated[str, Field(description="研报发布日期(yyyy-MM-dd, 如：2024-09-23), 默认为查询当天")] = None,
        size: Annotated[int, Field(description="获取研报数量，默认10")] = 10,
):
    """List all available reports.

    industry_code: 行业代码可以查询 tool `get_industry_code_by_name` 获取行业代码
    """
    if date is None:
        date = time.strftime("%Y-%m-%d", time.localtime())
    report = Report(
        code=code, industry_code=industry_code, begin_time=date,
        end_time=date, report_type=report_type, size=size)
    data = report.load()
    if len(data.data) > 0:
        df_data = data.to_frame()
        columns = ["title", "orgSName", "infoCode"]
        if "industryName" in df_data.columns:
            columns.append("industryName")
        return validate_response_data(df_data[columns])
    else:
        return "No data found."

@mcp.tool()
def fetch_report_text_by_code(
        info_code: Annotated[str, Field(description="研报信息代码")]
) -> str:
    """Fetch report data."""
    if re.match(r"^AP\d+$", info_code):
        report = Report()
        text = report.to_text(info_code=info_code)
        return text
    else:
        return "请输入正确的研报信息代码，如：`AP202505061668519723`"


@click.command()
@click.option("--port", "-p", default=8000, type=int, required=False, help="port")
@click.option("--transport", "-p", default="stdio", type=str, required=False, help="transport")
def report_mcp_server(
        transport: Literal["stdio", "sse"] = "stdio",
        port: Union[int, str] = None,
) -> None:
    """"""
    if transport == "sse":
        mcp.run(transport=transport, port=port)
    else:
        mcp.run(transport=transport)


if __name__ == "__main__":
    mcp.run(transport="sse", port=8002)
