import re
import os
import time
import click
from pydantic import Field
from fastmcp import FastMCP
from typing import Union, Optional, Literal, Annotated
from wisecon.report import Report, Announcement, AskSecretary
from wisecon.stock.index import ConceptionMap
from wisecon.mcp.validate import *
from mcp.server.session import ServerSession
from wisecon.types.request_api.report import TypeReport


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
        report_type: Annotated[TypeReport, Field(description="研报类型")],
        code: Annotated[str, Field(description="股票代码, 如600000")] = None,
        industry: Annotated[str, Field(description="行业名称，如 '军工'")] = None,
        industry_code: Annotated[Optional[Union[str, int]], Field(description="行业代码(如 '451'), '*' 为不限定行业")] = None,
        date: Annotated[str, Field(description="研报发布日期(yyyy-MM-dd, 如：2024-09-23), 默认为查询当天")] = None,
        size: Annotated[int, Field(description="获取研报数量，默认10")] = 10,
) -> str:
    """List all available reports.

    industry_code: 行业代码可以查询 tool `get_industry_code_by_name` 获取行业代码
    """
    if date is None:
        date = time.strftime("%Y-%m-%d", time.localtime())

    if industry_code is None:
        if industry is None:
            industry_code = "*"
        else:
            con_map = ConceptionMap()
            df_industry_choice = con_map.get_code_by_name(industry)
            if len(df_industry_choice) == 0:
                return f"Can't find industry `{industry}`"
            elif len(df_industry_choice) > 0:
                return f"Find multiple industry, Need choose one of the following industry code:\n\n{df_industry_choice.to_markdown(index=False)}"
            else:
                industry_code = df_industry_choice.bkCode.tolist()[0]

    if industry_code is not None:
        report_type: TypeReport = "行业研报"
    if code is not None:
        report_type: TypeReport = "个股研报"

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
def list_announcement(
        ann_type: Annotated[Literal["不限公告", "财务报告", "融资公告", "风险提示", "信息变更", "重大事项", "资产重组", "持股变动"], Field(description="公告类型")],
        date: Annotated[str, Field(description="公告日期, yyyy-MM-dd")],
        security_code: Annotated[str, Field(description="证券代码")] = None,
):
    """获取指定日期之后上市公司公布的公告列表，公告类型包括：不限公告、财务报告、融资公告、风险提示、信息变更、重大事项、资产重组、持股变动等

    Args:
        ann_type: 公告类型
        date: 公告日期，格式为yyyy-MM-dd，如`2023-01-01`为获取2023年1月1日之后公布的公告
        security_code: 证券代码，如`600000`，默认为空，表示获取所有证券的公告
    """
    ann = Announcement(node_name=ann_type, date=date, security_code=security_code)
    data = ann.load().to_frame()
    columns = ["art_code", "title", "codes", "columns", "notice_date"]
    return validate_response_data(data[columns])


@mcp.tool()
def ask_secretary(
        keyword: Annotated[str, Field(description="关键字")],
        start_date: Annotated[str, Field(description="开始日期, yyyy-MM-dd")],
        end_date: Annotated[str, Field(description="结束日期, yyyy-MM-dd")],
) -> str:
    """获取问董秘数据

    Args:
        keyword: 关键字，可以是股票代码、股票简称、股票名称等
        start_date: 开始日期，格式为yyyy-MM-dd
        end_date: 结束日期，格式为yyyy-MM-dd

    Returns:
    """
    columns = ["title", "content", "securityShortName", "responseTime", "headCharacter", "gubaId"]
    ask = AskSecretary(keyword=keyword, start_date=start_date, end_date=end_date, verbose=False)
    data = ask.load().to_frame()[columns].to_dict("records")
    return validate_response_data(data)


@mcp.tool()
def fetch_report_text_by_code(
        info_code: Annotated[str, Field(description="研报信息代码")]
) -> str:
    """Fetch report data."""
    if re.match(r"^AP\d+$", info_code):
        report = Report()
        text = report.to_text(info_code=info_code, tool="selenium")
        return text
    else:
        return "请输入正确的研报信息代码，如：`AP202505061668519723`"


@mcp.tool()
def remove_report_cache() -> str:
    """删除缓存的研报文件数据，返回删除的文件名列表。"""
    if os.getenv("WISECON_REPORT_DIR"):
        path = os.getenv("WISECON_REPORT_DIR")
    else:
        user_home = os.path.expanduser('~')
        path = os.path.join(user_home, "wisecon_report")

    files = os.listdir(path)
    if len(files) == 0:
        return "No report files found in cache."

    removed_files = []
    for file in files:
        if re.search(r"AP.*\.pdf$", file):
            os.remove(os.path.join(path, file))
            removed_files.append(file)
    return validate_response_data(removed_files)


@mcp.tool()
def get_tool_version() -> str:
    """获取当前工具的版本号"""
    from wisecon import __version__
    return __version__


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
