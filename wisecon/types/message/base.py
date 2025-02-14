from pydantic import BaseModel, Field
from typing import Literal, Dict


__all__ = [
    "Message",
    "ToolMessage"
]


class Message(BaseModel):
    role: str
    content: str

    def to_dict(self) -> Dict:
        return self.model_dump()


class ToolMessage(Message):
    """"""
    role: Literal["tool"] = Field(default="tool", description="角色")
    content: str = Field(default=None, description="对话内容")
    tool_call_id: str = Field(default=None, description="工具调用ID")
