# Report MCP Server

## 研报解读 MCP Server 配置

```json
{
  "mcpServers": {
    "wisecon-mcp": {
      "command": "uvx",
      "args": [
         "--from",
         "wisecon",
         "wisecon-report-server"
      ]
    }
  }
}
```

## 安装方式

### 需要先安装 uvx, wisecon>=0.1.8

```bash
# Windows安装脚本
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# MacOS和Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

*cherry-studio MCP环境安装[参考](https://docs.cherry-ai.com/advanced-basic/mcp/install)*

### 环境变量配置

- **Chrome Driver**：需要自己配置一下 [chrome driver](https://sites.google.com/chromium.org/driver/home)，并设置环境变量 `WISECON_CHROME_DRIVER_PATH`。需要注意下载与chrome版本一致的driver。
- **研报文件缓存路径**，可以选配研报保存的路径，设置环境变量 `WISECON_REPORT_DIR`，默认存储路径为 `/user/{user_name}/wisecon/report`

<figure markdown="span">
  ![Image title](../img/mcp/mcp-report-01.png){ width="800" }
  <figcaption>Cherry Studio 环境配置</figcaption>
</figure>

<figure markdown="span">
  ![Image title](../img/mcp/mcp-report-02.png){ width="800" }
  <figcaption>Chrome Driver 环境变量配置</figcaption>
</figure>

<figure markdown="span">
  ![Image title](../img/mcp/mcp-report-03.png){ width="800" }
  <figcaption>研报文件缓存路径配置</figcaption>
</figure>

### 使用方式

```text
uv run wisecon wisecon-stock-server --transport sse --port 8080

uvx --from wisecon wisecon-stock-server --transport sse --port 8080
```

*默认使用 stdio 方式，也可以使用 sse 方式，sse 需要指定 `--transport sse` 以及端口号 `--port 8080`*
