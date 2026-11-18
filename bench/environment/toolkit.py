from enum import Enum
from typing import Annotated, Any, Callable, Dict, Optional, TypeVar

from pydantic import BaseModel, Field

from bench.environment.db import DB
from bench.environment.tool import Tool, as_tool
from bench.utils import get_dict_hash, update_pydantic_model_with_dict

TOOL_ATTR = "__tool__"
TOOL_TYPE_ATTR = "__tool_type__"

# DB 哈希 / 响应比较时需排除的字段：
#   时间戳字段（每次执行时间不同）
_TS_FIELDS = {"created_at", "updated_at", "acted_at", "finalized_at"}
#   自由文本字段（agent 自由填写，golden action 用占位符，无法精确匹配）
_FREE_TEXT_FIELDS = {"comment", "manager_comment", "notes", "bio"}
#   业务编号字段：ticket_code 由调用方自填（golden 写死值不可推）；ticket_number/request_number
#   为工具运行时自动铸号（含年份，历史上随真实时钟漂移）——均不应参与终态哈希比对
_BIZ_NUMBER_FIELDS = {"ticket_code", "ticket_number", "request_number"}

_UNSTABLE_FIELDS = _TS_FIELDS | _FREE_TEXT_FIELDS | _BIZ_NUMBER_FIELDS


def strip_timestamps(obj):
    """递归剔除时间戳和自由文本字段，用于 get_db_hash() 和 set_state 响应比较。"""
    if isinstance(obj, dict):
        # 统一剔除 *_at 字段，避免 requested_at/assigned_at/issued_at 等动态时间戳导致重放不稳定
        return {
            k: strip_timestamps(v)
            for k, v in obj.items()
            if k not in _UNSTABLE_FIELDS and not str(k).endswith("_at")
        }
    if isinstance(obj, list):
        return [strip_timestamps(i) for i in obj]
    return obj


# 保留旧名兼容内部调用
_strip_timestamps = strip_timestamps


T = TypeVar("T", bound=DB)

COUNTER = 0

class ToolKitType(type):
    """Metaclass for ToolKit classes."""

    def __init__(cls, name, bases, attrs):
        func_tools = {}
        for name, method in attrs.items():
            if isinstance(method, property):
                method = method.fget
            if hasattr(method, TOOL_ATTR):
                func_tools[name] = method
        # global COUNTER
        # COUNTER += 1
        # print(30,COUNTER,cls)
        # if COUNTER==6:
        #     print(27,func_tools)
        #     print('\n\n')
        #     raise ValueError('debug')

        @property
        def _func_tools(self) -> Dict[str, Callable]:
            """Get the tools available in the ToolKit."""
            all_func_tools = func_tools.copy()
            try:
                all_func_tools.update(super(cls, self)._func_tools)
            except AttributeError:
                pass
            return all_func_tools

        cls._func_tools = _func_tools


class ToolType(str, Enum):
    """Type of a tool."""

    READ = "read"
    WRITE = "write"
    THINK = "think"
    GENERIC = "generic"


def is_tool(tool_type: ToolType = ToolType.READ):
    """Decorator to mark a function as a tool.

    Args:
        write: Whether this tool modifies state (True) or just reads state (False)
    """

    def decorator(func):
        setattr(func, TOOL_ATTR, True)
        setattr(func, TOOL_TYPE_ATTR, tool_type)
        return func

    return decorator


class ToolKitBase(metaclass=ToolKitType):
    """Base class for ToolKit classes."""

    def __init__(self, db: Optional[T] = None):
        self.db: Optional[T] = db

    @property
    def tools(self) -> Dict[str, Callable]:
        """Get the tools available in the ToolKit."""
        return_tools = {name: getattr(self, name) for name in self._func_tools.keys()}
        # print(75,return_tools)
        # exit(0)
        return return_tools

    def use_tool(self, tool_name: str, **kwargs) -> str:
        """Use a tool."""
        if tool_name not in self.tools:
            raise ValueError(f"Tool '{tool_name}' not found.")
        return self.tools[tool_name](**kwargs)

    def get_tools(self) -> Dict[str, Tool]:
        """Get the tools available in the ToolKit.
        Uses the `as_tool` to convert the functions to Tool objects.

        Returns:
            A dictionary of tools available in the ToolKit.
        """
        # NOTE: as_tool needs to get the function (self.foo), not the `foo(self, ...)`
        # Otherwise, the `self` will exists in the arguments.
        # Therefore, it needs to be called with getattr(self, name)
        return {name: as_tool(tool) for name, tool in self.tools.items()}

    def has_tool(self, tool_name: str) -> bool:
        """Check if a tool exists in the ToolKit."""
        return tool_name in self.tools

    def tool_type(self, tool_name: str) -> ToolType:
        """Get the type of a tool."""
        return getattr(self.tools[tool_name], TOOL_TYPE_ATTR)

    def get_statistics(self) -> dict[str, Any]:
        """Get the statistics of the ToolKit."""
        num_tools = len(self.tools)
        num_read_tools = sum(
            self.tool_type(name) == ToolType.READ for name in self.tools
        )
        num_write_tools = sum(
            self.tool_type(name) == ToolType.WRITE for name in self.tools
        )
        num_think_tools = sum(
            self.tool_type(name) == ToolType.THINK for name in self.tools
        )
        num_generic_tools = sum(
            self.tool_type(name) == ToolType.GENERIC for name in self.tools
        )
        return {
            "num_tools": num_tools,
            "num_read_tools": num_read_tools,
            "num_write_tools": num_write_tools,
            "num_think_tools": num_think_tools,
            "num_generic_tools": num_generic_tools,
        }

    def update_db(self, update_data: Optional[dict[str, Any]] = None):
        """Update the database of the ToolKit."""
        if update_data is None:
            update_data = {}
        if self.db is None:
            raise ValueError("Database has not been initialized.")
        self.db = update_pydantic_model_with_dict(self.db, update_data)

    def get_db_hash(self) -> str:
        """Get the hash of the database.

        时间戳字段（created_at / updated_at）在哈希前被递归剔除。
        原因：submit 类工具（如 submit_leave_request）内部调用 _now_iso() 写入
        created_at，该值取自 datetime.now()，在 gold environment 和 predicted
        environment 两次独立执行中必然不同，若保留则 DB hash 永远不匹配。
        而 _generate_ref() 基于 len(collection)+1 是确定性的，ref 本身完全可
        重现，因此只需排除时间戳字段即可让 submit 任务也能使用 DB 奖励验证。
        """
        return get_dict_hash(_strip_timestamps(self.db.model_dump()))


class ToolSignature(BaseModel):
    """A signature of a tool."""

    name: Annotated[str, Field(description="The name of the tool")]
    doc: Annotated[str, Field(description="The documentation of the tool")]
    params: Annotated[
        Optional[dict],
        Field(description="JSON schema of the parameters of the tool", default=None),
    ]
    returns: Annotated[
        Optional[dict],
        Field(description="JSON schema of the return of the tool", default=None),
    ]


def get_tool_signatures(tools: ToolKitBase) -> dict[str, ToolSignature]:
    """Get all the tool signatures from a tool kit.

    Returns:
        A dictionary of tool signatures.
    """
    signatures = {}
    for name, tool in tools.get_tools().items():
        signatures[name] = ToolSignature(
            name=name,
            doc=str(tool),
            params=tool._serialize_params(tool.params),
            returns=tool._serialize_returns(tool.returns),
        )
    return signatures


def get_tool_types(tools: ToolKitBase) -> dict[str, ToolType]:
    """Get the type of a tool.

    Returns:
        A dictionary of tool types.
    """
    return {name: tools.tool_type(name) for name in tools.get_tools().keys()}


class GenericToolKit(ToolKitBase):
    """Defines some generic tools.
    - Think
    - Calculate
    """

    @is_tool(ToolType.THINK)
    def think(self, thought: str) -> str:
        """
        Use the tool to think about something. It will not obtain new information or change the database, but just append the thought to the log. Use it when complex reasoning is needed.

        Args:
            thought: A thought to think about.

        Returns:
            Empty string
        """
        return ""

    @is_tool(ToolType.GENERIC)
    def calculate(self, expression: str) -> str:
        """
        Calculate the result of a mathematical expression.

        Args:
            expression: The mathematical expression to calculate, such as '2 + 2'. The expression can contain numbers, operators (+, -, *, /), parentheses, and spaces.

        Returns:
            The result of the mathematical expression.

        Raises:
            ValueError: If the expression is invalid.
        """
        if not all(char in "0123456789+-*/(). " for char in expression):
            raise ValueError("Invalid characters in expression")
        return str(round(float(eval(expression, {"__builtins__": None}, {})), 2))
