import os
from logging import Logger
from openai import OpenAI
from zhipuai import ZhipuAI
from pydantic import BaseModel, ConfigDict
from typing import Any, List, Callable, Optional, Literal, Union
from openai._streaming import Stream
from openai.types.chat.chat_completion import (
    ChatCompletion)
from openai.types.chat.chat_completion_chunk import (
    ChatCompletionChunk, Choice, ChoiceDelta)

from wisecon.types.message import Message, ToolMessage
from wisecon.agent.tools.tools import Tools
from wisecon.utils.logger import LoggerMixin


__all__ = ["BaseAgent"]


class BaseAgent(BaseModel, LoggerMixin):
    """
    todo: 1. 区分Agent模型与Reasoning模型
    todo: 2. 增加sse模式
    """
    model_config = ConfigDict(arbitrary_types_allowed=True)
    client: Union[OpenAI, ZhipuAI, Literal["openai", "zhipu"]]
    model: str
    api_key: Optional[str]
    api_key_name: Optional[str]
    base_url: str
    tools: Tools

    def __init__(
            self,
            model: str,
            api_key: Optional[str] = None,
            base_url: Optional[str] = "https://api.openai.com/v1",
            api_key_name: Optional[str] = None,
            tools: List[Any] = None,
            client: Union[OpenAI, ZhipuAI, Literal["openai", "zhipu"]] = "openai",
            logger: Optional[Union[Logger, Callable]] = None,
            verbose: Optional[bool] = True,
            **kwargs
    ):
        """"""
        super().__init__(
            api_key=api_key, base_url=base_url, model=model,
            tools=tools, api_key_name=api_key_name,
            client=client, logger=logger, verbose=verbose,
            **kwargs)
        self.set_api_key(api_key, api_key_name)
        self.set_client(client)
        self.logger = logger
        self.verbose = verbose

    def set_client(
            self,
            client: Union[OpenAI, ZhipuAI, Literal["openai", "zhipu"]] = "openai",
    ):
        """"""
        if isinstance(client, (OpenAI, ZhipuAI)):
            self.client = client
        elif client == "zhipu":
            self.client = ZhipuAI(api_key=self.api_key, base_url=self.base_url)
        elif client == "openai":
            self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        else:
            raise ValueError(f"Client `{client}` is not supported.")

    def set_api_key(self, api_key: Optional[str] = None, api_key_name: Optional[str] = None):
        """"""
        if api_key is not None:
            self.api_key = api_key
        elif api_key_name is not None:
            self.api_key = os.getenv(self.api_key_name)
        if self.api_key is None:
            raise ValueError("API key not found")

    def _chunk(
            self,
            role: Optional[Literal["developer", "system", "user", "assistant", "tool"]],
            content: str,
            chunk: ChatCompletionChunk,
    ) -> ChatCompletionChunk:
        """"""
        choices = [Choice(delta=ChoiceDelta(role=role, content=content), index=0)]
        return ChatCompletionChunk(
            choices=choices, id=chunk.id, created=chunk.created, model=chunk.model,
            object="chat.completion.chunk")

    def chat(
            self,
            prompt: Optional[str] = None,
            messages: Optional[List[Message]] = None,
            stream: Optional[bool] = False
    ) -> Union[ChatCompletion | Stream[ChatCompletionChunk]]:
        """"""
        if stream:
            return self.sse(prompt, messages)
        else:
            return self.sync(prompt, messages)

    def sync(
            self,
            prompt: Optional[str] = None,
            messages: Optional[List[Message]] = None,
    ) -> ChatCompletion:
        """"""
        if prompt is not None:
            messages = [Message(role="user", content=prompt)]
        self._logger(msg=f"[User] {messages[-1].content}\n", color="blue")

        completion = self.client.chat.completions.create(
            model=self.model, messages=[msg.to_dict() for msg in messages], tools=self.tools.descriptions)

        if completion.choices[0].finish_reason == "tool_calls":
            messages.append(completion.choices[0].message)
            function = completion.choices[0].message.tool_calls[0].function
            self._logger(msg=f"[Assistant] name: {function.name}, arguments: {function.arguments}\n", color="green")

            observation = self.tools.dispatch(function=function)
            self._logger(msg=f"[Observation] \n{observation}\n", color="magenta")

            messages.append(ToolMessage(role="tool", content=observation, tool_call_id=completion.choices[0].message.tool_calls[0].id))
            completion = self.client.chat.completions.create(
                model=self.model, messages=[msg.to_dict() for msg in messages], tools=self.tools.descriptions)
        content = completion.choices[0].message.content
        self._logger(msg=f"[Assistant] {content}\n", color="green")
        return completion

    def sse(
            self,
            prompt: Optional[str] = None,
            messages: Optional[List[Message]] = None,
    ) -> Stream[ChatCompletionChunk]:
        """"""
        if prompt is not None:
            messages = [Message(role="user", content=prompt)]

        completion = self.client.chat.completions.create(
            model=self.model, messages=[msg.to_dict() for msg in messages], tools=self.tools.descriptions, stream=True)

        chunk = None
        function = None
        tool_call_id = None
        for chunk in completion:
            if chunk.choices[0].delta.tool_calls:
                function = chunk.choices[0].delta.tool_calls[0].function
                tool_call_id = chunk.choices[0].delta.tool_calls[0].id
                messages.append(chunk.choices[0].delta)
            yield chunk

        if function is not None:
            yield self._chunk(role="assistant", content="\n\n", chunk=chunk)
            observation = self.tools.dispatch(function=function)
            yield self._chunk(role="tool", content=observation, chunk=chunk)
            yield self._chunk(role="tool", content="\n\n", chunk=chunk)
            messages.append(
                ToolMessage(role="tool", content=observation, tool_call_id=tool_call_id))
            completion = self.client.chat.completions.create(
                model=self.model, messages=[msg.to_dict() for msg in messages],
                tools=self.tools.descriptions, stream=True)
            for chunk in completion:
                yield chunk
