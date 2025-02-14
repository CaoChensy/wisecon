import traceback
from pydantic import BaseModel, Field
from typing import Any, List, Dict, Optional, Callable
from wisecon.types.agent import Function
from wisecon.agent.tools.register import register_tool


__all__ = [
    "Tools",
]


class Tools(BaseModel):
    """"""
    descriptions: List[Dict] = Field(default=[], description="Description of the tool")
    hooks: Dict[str, Callable] = Field(default={}, description="Hooks of the tool")
    tools: List[Callable] = Field(default=None, description="List of function to be used as tools")
    params_fun: Optional[Callable] = Field(default=None, description="Function to clean the parameters of the tool")

    def __init__(self, tools: List[Callable], **kwargs):
        super().__init__(tools=tools, **kwargs)
        self.register_tools()

    def register_tools(self):
        """"""
        _ = [register_tool(hooks=self.hooks, descriptions=self.descriptions)(fun)for fun in self.tools]

    def dispatch(self, function: Function) -> Any:
        """"""
        function = Function.model_validate(function.model_dump())
        if function.name not in self.hooks:
            return f"Tool `{function.name}` not found. Please use a provided tool."
        tool_call = self.hooks[function.name]
        try:
            data = tool_call(**function.arguments).load()
            ret = data.to_frame(chinese_column=True).to_markdown()
        except:
            ret = traceback.format_exc()
        return ret
