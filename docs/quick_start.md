# Quick Start

> 这是一个快速开始指南，你可以通过这个指南在`10min`的时间里来了解如何使用ZLAI。

## 项目简介

[![Python package](https://img.shields.io/pypi/v/zlai)](https://pypi.org/project/zlai/)
[![Python](https://img.shields.io/pypi/pyversions/zlai.svg)](https://pypi.python.org/pypi/zlai/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/zlai)](https://pypi.org/project/zlai/)
[![GitHub star chart](https://img.shields.io/github/stars/zlai-llm/zlai?style=flat-square)](https://star-history.com/#zlai-llm/zlai)
[![GitHub Forks](https://img.shields.io/github/forks/zlai-llm/zlai.svg)](https://star-history.com/#zlai-llm/zlai)
[![Doc](https://img.shields.io/badge/Doc-online-green)](https://zlai-llm.github.io/zlai-doc/)
[![Issue](https://img.shields.io/github/issues/zlai-llm/zlai)](https://github.com/zlai-llm/zlai/issues/new/choose)
[![Discussions](https://img.shields.io/github/discussions/zlai-llm/zlai)](https://github.com/zlai-llm/zlai/issues/new/choose)
[![CONTRIBUTING](https://img.shields.io/badge/Contributing-8A2BE2)](https://github.com/zlai-llm/zlai/blob/main/CONTRIBUTING.md)
[![License: MIT](https://img.shields.io/github/license/zlai-llm/zlai)](https://github.com/zlai-llm/zlai/blob/main/LICENSE)

> 项目结构

<center>
<img src="./img/zlai-overview.png" width="980px">
<h5>Fig. Project-ZLAI</h5>
</center>

> ZLAI模块简介

1. `LLM`: 调用大模型的便捷方法，包括本地大模型与线上大模型，其中包括主流大模型`API`，`GLM/Qwen/Yi/MoonShot`等100多种大模型。采用了统一的调用风格与方式，使得大模型调用更加便捷。
2. `Message`: 消息管理机制，方便管理`System/User/Assistant Message`，并进行大模型对话的记忆管理。
3. `Embedding`: 提供一系列向量化方法，包括本地与API向量化模型的调用，以及文本的各类向量化匹配、与向数据库对接等功能。
4. `RAG`: 提供一系列文档知识库问答方法。
5. `AgentTask`: 提供Agent任务流的调度，实现Agent任务的各种自动化流转。
6. `AgentTools`: 提供一系列Agent工具函数，实现更方便的Agent使用，如让大模型实现股票期货数据查询问答、数据分析作图等。
7. `Other`: 其他便捷方法。

*这就是目前ZLAI的项目结构，下面将深入实践ZLAI的大模型开发。*

## 如何安装？

```bash
# [推荐] 安装最新版本ZLAI的所有模块
pip install zlai[all] -U
# [推荐] 最轻量化安装
pip install zlai[tiny] -U
# [推荐] 安装全部大模型API依赖
pip install zlai[api] -U
```

```bash
# [echarts] 安装了 echarts 模块
pip install zlai[echarts] -U
# [vector_db] 安装了向量数据库模块
pip install zlai[vector_db] -U
# [langchain] 安装了 langchain 模块
pip install zlai[langchain] -U
# [database] 安装了数据库相关模块
pip install zlai[database] -U
# [streamlit] 安装了 streamlit 模块
pip install zlai[streamlit] -U
```

您也可以在[GitHub](https://github.com/zlai-llm/zlai.git)/[PyPi](https://pypi.org/project/zlai/)查看最新代码与最新发行版本。

## 如何调用大模型？

在调用大模型之前，你需要首先配置各类大模型API的环境变量`API-Key`，可以[参考](llm/zlai-llm-01?id=api-key)。

> 我们以智谱AI的`GLM4-Air`为例，构建一个大模型调用示例。下面是示例代码：

```python
from zlai.llms import Zhipu, GLM4AirGenerateConfig

llm = Zhipu(generate_config=GLM4AirGenerateConfig())

completion = llm.generate("你好。")
print(completion.choices[0].message.content)
```

*输出*

```text
你好👋！我是人工智能助手智谱清言（ChatGLM），很高兴见到你，欢迎问我任何问题。
```

- `Zhipu` 是一个大模型调用类
- `GLM4AirGenerateConfig` 是一个大模型配置类
- `.generate` 方法是调用大模型的推理方法

在`zlai`中您可以使用类似的方式调用100多种国内主流大模型`API`，详细介绍可以查询[大模型API调用](llm/zlai-llm-01.md)。在[大模型参数理论解析](llm/zlai-llm-04.md)与[大模型参数的设定](prompt/zlai-prompt-03.md)中，我们详细介绍了大模型参数设定的原理与实践。相信了解这些您可以更加灵活的调整大模型的推理参数以获取更为准确、丰富的回答。

此外，在[大模型调用的便捷方法](llm/zlai-llm-02.md)中我们更详细的说明了`zlai`中对于大模型调用的形式，如全量推理、流式推理等，如果您想使用本地大模型也可以参考[本地大模型](llm/zlai-llm-openai-api.md)。

## 如何让大模型拥有记忆？

**消息组织机制是大模型对话以及Agent应用的基础**，灵活方便地管理`System/User/Assistant Message`，可以实现多种复杂问答与记忆管理。

```python
from zlai.schema import *
from zlai.llms import Zhipu, GLM4AirGenerateConfig

messages = [
    SystemMessage(content="你是一个人工智能助手。用于记录我的日常事务。"),
    UserMessage(content="你好，我的好朋友六子昨天早晨吃了2碗粉。"),
    AssistantMessage(content="好的，我记住了。")
]

llm = Zhipu(generate_config=GLM4AirGenerateConfig())

# 新的问题
messages.append(UserMessage(content="请问，昨天六子早上吃了几碗粉？"))
completion = llm.generate(messages=messages)
print(completion.choices[0].message.content)
```

*输出*

```text
昨天六子早上吃了2碗粉。
```

你看，在上面的示例中，我们通过`messages`参数传递的方式，让大模型拥有了记忆，从而实现多轮对话与记忆管理。在[消息机制](message/zlai-message-01.md)章节中我们可以详细了解到`ZLAI`对于消息内容的管理机制，包括`System/User/Assistant Message`的存储、管理、查询等。

## 如何设计好的提示词？

> 提示词`Prompt`是大模型对话与Agent应用的基础，那么，如何设计一个好的提示词呢？您可以参考以下章节：

- [大模型的局限性](prompt/zlai-prompt-01.md)
- [提示词设计一般思路](prompt/zlai-prompt-02.md)
- [Few-shot提示](prompt/zlai-prompt-04.md)
- [事实知识提示](prompt/zlai-prompt-05.md)
- [思维链](prompt/zlai-prompt-06.md)
- [自我一致性](prompt/zlai-prompt-07.md)
- [检索增强生成](prompt/zlai-prompt-08.md)
- [提示词应用](prompt-apply/zlai-prompt-apply-01.md)   
- [生成数据](prompt-apply/zlai-prompt-apply-02.md)    
- [文本分类](prompt-apply/zlai-prompt-apply-03.md)    
- [结构化数据解析](prompt-apply/zlai-prompt-apply-04.md) 
- [总结文本摘要](prompt-apply/zlai-prompt-apply-06.md)  
- [代码生成](prompt-apply/zlai-prompt-apply-07.md)    
- [对话](prompt-apply/zlai-prompt-apply-08.md)     

## 大模型与向量化技术

- [文本的数字化表示](embedding/zlai-embedding-01.md)      
- [向量化在大模型中的应用](embedding/zlai-embedding-02.md)   
- [向量数据库简介](embedding/zlai-embedding-03.md)       
- [elasticsearch](embedding/zlai-elasticsearch.md)
- [milvus](embedding/milvus.md)                   
- [RAG](rag/zlai-rag-01.md)    

## 如何构建Agent?

* [ZLAI-Agent架构介绍](agent/zlai-agent-01.md)
* [ZLAI-ToolsAgent](agent/zlai-agent-tools.md)
* [ZLAI-Charts-Tools](agent/zlai-charts-tools)
* [公募基金问答](agent/zlai-agent-fund)
* [天气查询](agent/zlai-agent-02.md)
* [RAG增强索引](agent/zlai-agent-rag)
* [Bing搜索增强问答](agent/zlai-agent-bing)
* [数据库查询](agent/zlai-agent-03.md)
* [CSV数据查询](agent/zlai-agent-04.md)
* [Shell命令](agent/zlai-agent-07)
* [股票问答](agent/zlai-agent-09)
* [其他问答](agent/zlai-agent-10)

## 其他工具

- [document](parse/zlai-document.md)              
- [parse](parse/zlai-parse-01.md)                 

## End

----
@2024/07/01

todo: 完善Agent之后的部分
