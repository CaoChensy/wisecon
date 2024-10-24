# 新闻数据

## 获取新闻列表

> 可选择新闻主题

`["财经导读", "产经新闻", "国内经济", "国际经济", "证券聚焦", "纵深调查", "经济时评", "产业透视", "商业观察", "股市评论", "商业资讯", "创业研究", "A股公司", "港股公司", "中概股公司", "海外公司",]`

> 示例

```python
from zlai.tools.report.news import *

news = News(size=20)
data = news.load_data()
print(data.metadata)
print(data.to_frame(columns=data.metadata.get("columns")).to_markdown())
```

## 获取新闻详情

> 示例

```python
url = "http://finance.eastmoney.com/news/1344,202409293194209890.html"
news = News(size=10)
content = news.load_content(url)
print(content)
```

## 获取新闻主题

> 示例

```python
from zlai.tools.report.news import *

news = News(size=10, theme="国际经济")
data = news.load_data()
print(data.metadata)
print(data.to_frame(columns=data.metadata.get("columns")))
```

----
