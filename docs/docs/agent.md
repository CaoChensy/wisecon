# 使用Wisecon-Agent调用数据

> 现在，Wisecon-Agent已经原生支持大模型通过Function Call方式调用数据并进行数据分析啦。使用步骤是下面：

**1. 配置API工具**

```python
from wisecon.agent import *
from wisecon.movie import *
from wisecon.stock.etf import *
from wisecon.stock.market import *
from wisecon.stock.financial import *
from wisecon.stock.kline import *
from wisecon.stock.tick import *

tools = Tools(tools=[
    LastDayMarketSummary, # 获取昨日市场整体交易数据
    KLine,                # 获取K线数据
    KlineMin,             # 获取分钟级K线数据
    Tick,                 # 获取逐笔数据
    StockBalance,         # 获取股票资产负债表数据
    ETFGoldHistory,       # 获取黄金ETF历史数据
    TV, Movie             # 获取电影票房、电视收视率信息等数据
])
```

**2. 配置大模型Agent**

```python
from wisecon.agent import BaseAgent    

base_url = "https://open.bigmodel.cn/api/paas/v4"
agent = BaseAgent(
    model="glm-4-flash", 
    base_url=base_url, 
    tools=tools,                   # 上面配置的API工具
    api_key="your api key",        # 你的API Key, 如果配置了环境变量（api_key_name），可以不填
    api_key_name="ZHIPU_API_KEY"   # API Key的名称
)
```

**3. 使用大模型Agent问答查询**

???+ question "现在最受新欢的电影是哪部?"

    === "代码示例"

        ```python
        completion = agent.chat("现在最受新欢的电影是哪部？")
        ```

    === "数据调用"

        ```markdown
        [User] 现在最受新欢的电影是哪部
        
        [Assistant] name: Movie, arguments: {}
        
        [Observation] 
        |    |   票房描述 | 票房占比   | 座位使用率   | 场次占比   | 总票房描述   |   电影ID | 电影名称             | 上映信息   |
        |---:|-----------:|:-----------|:-------------|:-----------|:-------------|---------:|:---------------------|:-----------|
        |  0 |    9354.54 | 82.9%      | 68.1%        | 58.5%      | 122.94亿     |  1294273 | 哪吒之魔童闹海       | 上映22天   |
        |  1 |     851.46 | 7.5%       | 12.9%        | 16.4%      | 32.39亿      |  1492100 | 唐探1900             | 上映22天   |
        |  2 |     386.04 | 3.4%       | 2.0%         | 2.2%       | 837.7万      |  1551329 | 您的声音             | 上映2天    |
        |  3 |     170.49 | 1.5%       | 3.5%         | 5.1%       | 11.66亿      |  1245203 | 封神第二部：战火西岐 | 上映22天   |
        |  4 |     140.84 | 1.2%       | 3.2%         | 4.3%       | 4139.9万     |      685 | 花样年华             | 上映6天    |
        |  5 |     126.63 | 1.1%       | 5.3%         | 6.6%       | 8466.7万     |  1427283 | 美国队长4            | 上映6天    |
        |  6 |     114.98 | 1.0%       | 2.7%         | 3.5%       | 7.39亿       |  1529787 | 熊出没·重启未来      | 上映22天   |
        |  7 |     102.71 | 0.9%       | 1.6%         | 2.3%       | 6.49亿       |  1490902 | 射雕英雄传：侠之大者 | 上映22天   |
        |  8 |       8.53 | <0.1%      | <0.1%        | <0.1%      | 3.89亿       |  1379087 | 蛟龙行动             | 上映22天   |
        |  9 |       3.91 | <0.1%      | <0.1%        | <0.1%      | 8163.6万     |  1467290 | 雄狮少年2            | 上映68天   |
        ```

    === "回答结果"

        **目前最受新欢的电影是《哪吒之魔童闹海》，其票房占比为82.9%，座位使用率为68.1%，场次占比为58.5%，总票房达到了122.94亿。该电影已经上映了22天。**

???+ question "当前300069股票最近5分钟的最低价价格是多少?"

    === "代码示例"

        ```python
        completion = agent.chat("当前300069股票最近5分钟的最低价价格是多少？")
        ```

    === "数据调用"

        ```markdown
        [User] 当前300069股票最近5分钟的最低价价格是多少？

        [Assistant] name: KLine, arguments: {"security_code": "300069", "period": "5m", "size": 1}
        
        [Observation] 
        |    | 时间             |   开盘 |   收盘 |   最高 |   最低 |   成交量 |      成交额 |   振幅 |   涨跌幅 |   涨跌额 |   换手率 |
        |---:|:-----------------|-------:|-------:|-------:|-------:|---------:|------------:|-------:|---------:|---------:|---------:|
        |  0 | 2025-02-19 15:00 |  17.32 |   17.3 |  17.32 |  17.28 |     3522 | 6.09349e+06 |   0.23 |    -0.12 |    -0.02 |      0.3 |
        ```

    === "回答结果"

        **当前300069股票最近5分钟的最低价价格是17.28元。**



----
