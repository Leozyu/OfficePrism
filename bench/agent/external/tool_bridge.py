"""通用工具桥接层。

将 OfficePrism 的 (OpenAI tool schema, call_tool callback) 转换为各 package 的原生工具格式。
"""

import json
import inspect
from typing import Any, Callable


_TYPE_MAP_STR = {"string": "str", "integer": "int", "number": "float", "boolean": "bool", "array": "list", "object": "dict"}
_TYPE_MAP_CLS = {"string": str, "integer": int, "number": float, "boolean": bool, "array": list, "object": dict}


def _build_func_from_schema(
    schema: dict,
    call_tool: Callable[[str, dict], str],
) -> Callable:
    """从 OpenAI tool schema + call_tool 回调生成一个有正确签名和 __annotations__ 的 Python 函数。

    使用 exec 动态生成，确保 pydantic / autogen / langchain 能正确解析参数。
    """
    func_def = schema.get("function", schema)
    func_name = func_def["name"]
    description = func_def.get("description", func_name)
    params = func_def.get("parameters", {})
    properties = params.get("properties", {})
    required = set(params.get("required", []))

    # 构建 docstring
    doc_parts = [description]
    if properties:
        doc_parts.append("\nArgs:")
        for pname, pinfo in properties.items():
            pdesc = pinfo.get("description", "")
            doc_parts.append(f"    {pname}: {pdesc}")
    docstring = "\n".join(doc_parts)

    # 构建函数签名字符串（带类型标注）
    sig_parts = []
    annotations: dict[str, type] = {}
    for pname, pinfo in properties.items():
        ptype = pinfo.get("type", "string")
        py_type_str = _TYPE_MAP_STR.get(ptype, "str")
        annotations[pname] = _TYPE_MAP_CLS.get(ptype, str)
        if pname in required:
            sig_parts.append(f"{pname}: {py_type_str}")
        else:
            default = pinfo.get("default", None)
            sig_parts.append(f"{pname}: {py_type_str} = {repr(default)}")

    params_str = ", ".join(sig_parts)
    annotations["return"] = str

    code = f"def {func_name}({params_str}) -> str:\n"
    code += f"    '''{docstring}'''\n"
    code += f"    _kwargs = {{}}\n"
    for pname in properties:
        code += f"    if {pname} is not None:\n"
        code += f"        _kwargs[{repr(pname)}] = {pname}\n"
    code += f"    return _call_tool({repr(func_name)}, _kwargs)\n"

    ns: dict[str, Any] = {"_call_tool": call_tool}
    exec(code, ns)
    fn = ns[func_name]
    fn.__annotations__ = annotations
    return fn


def to_langchain_tools(
    tools_schema: list[dict],
    call_tool: Callable[[str, dict], str],
) -> list:
    """将 OpenAI tool schema 列表转为 langchain StructuredTool 列表。"""
    try:
        from langchain_core.tools import StructuredTool
        from pydantic import create_model, Field
    except ImportError:
        raise ImportError("pip install langchain-core pydantic")

    type_map = {"string": str, "integer": int, "number": float, "boolean": bool, "array": list, "object": dict}

    lc_tools = []
    for schema in tools_schema:
        func_def = schema.get("function", schema)
        func_name = func_def["name"]
        description = func_def.get("description", func_name)
        params = func_def.get("parameters", {})
        properties = params.get("properties", {})
        required = set(params.get("required", []))

        # 用 pydantic create_model 构建 args_schema，避免 from_function 的 type hints 问题
        fields = {}
        for pname, pinfo in properties.items():
            py_type = type_map.get(pinfo.get("type", "string"), str)
            pdesc = pinfo.get("description", "")
            if pname in required:
                fields[pname] = (py_type, Field(description=pdesc))
            else:
                fields[pname] = (py_type, Field(default=None, description=pdesc))

        args_model = create_model(f"{func_name}_args", **fields)

        _call_tool = call_tool
        _func_name = func_name

        def make_fn(ct, fn):
            def _fn(**kwargs) -> str:
                return ct(fn, kwargs)
            _fn.__name__ = fn
            _fn.__doc__ = description
            return _fn

        tool = StructuredTool(
            name=func_name,
            description=description,
            func=make_fn(_call_tool, _func_name),
            args_schema=args_model,
        )
        lc_tools.append(tool)
    return lc_tools


def to_smolagents_tools(
    tools_schema: list[dict],
    call_tool: Callable[[str, dict], str],
) -> list:
    """将 OpenAI tool schema 列表转为 smolagents Tool 列表。"""
    try:
        from smolagents import Tool as SmolTool
    except ImportError:
        raise ImportError("pip install smolagents")

    def _make_smol_tool(func_def: dict, call_tool_fn: Callable) -> SmolTool:
        """为单个 schema 创建 smolagents Tool 实例。

        smolagents 要求 forward 方法的参数名与 inputs 的 keys 完全匹配，
        因此用 exec 动态生成函数签名。
        """
        _name = func_def["name"]
        _desc = func_def.get("description", _name)
        _properties = func_def.get("parameters", {}).get("properties", {})
        _required = set(func_def.get("parameters", {}).get("required", []))

        _type_map = {"string": "string", "integer": "integer", "number": "number",
                      "boolean": "boolean", "array": "array", "object": "object"}

        _inputs = {}
        param_names = []
        for pname, pinfo in _properties.items():
            _inputs[pname] = {
                "type": _type_map.get(pinfo.get("type", "string"), "string"),
                "description": pinfo.get("description", ""),
            }
            if pname not in _required:
                _inputs[pname]["nullable"] = True
            param_names.append(pname)

        # 动态生成 forward 方法，签名匹配 inputs keys
        # nullable 参数需要默认值 None
        sig_parts = []
        for pname in param_names:
            if pname not in _required:
                sig_parts.append(f"{pname}=None")
            else:
                sig_parts.append(pname)

        if param_names:
            params_str = ", ".join(sig_parts)
            # 过滤掉 None 值参数，避免传递未设置的可选参数
            code = f"def forward(self, {params_str}):\n"
            code += f"    _args = {{}}\n"
            for pname in param_names:
                code += f"    if {pname} is not None:\n"
                code += f"        _args[{repr(pname)}] = {pname}\n"
            code += f"    return _ct(_fn, _args)\n"
        else:
            code = "def forward(self):\n    return _ct(_fn, {})\n"

        ns: dict[str, Any] = {"_ct": call_tool_fn, "_fn": _name}
        exec(code, ns)
        forward_fn = ns["forward"]

        tool_cls = type(
            f"SmolTool_{_name}",
            (SmolTool,),
            {
                "name": _name,
                "description": _desc,
                "inputs": _inputs,
                "output_type": "string",
                "forward": forward_fn,
                "is_initialized": True,
            },
        )
        return tool_cls()

    smol_tools = []
    for schema in tools_schema:
        func_def = schema.get("function", schema)
        smol_tools.append(_make_smol_tool(func_def, call_tool))

    return smol_tools


def to_autogen_tools(
    tools_schema: list[dict],
    call_tool: Callable[[str, dict], str],
) -> list:
    """将 OpenAI tool schema 列表转为 autogen FunctionTool 列表。"""
    try:
        from autogen_core.tools import FunctionTool
    except ImportError:
        raise ImportError("pip install autogen-core")

    ag_tools = []
    for schema in tools_schema:
        func = _build_func_from_schema(schema, call_tool)
        func_def = schema.get("function", schema)
        tool = FunctionTool(func, description=func_def.get("description", func_def["name"]))
        ag_tools.append(tool)
    return ag_tools


def split_tools_by_function(tools_schema: list[dict]) -> dict[str, list[dict]]:
    """按功能分组工具（查询/操作/审批），用于 multi-agent 工具分配。"""
    groups: dict[str, list[dict]] = {"query": [], "action": [], "other": []}
    for schema in tools_schema:
        func_def = schema.get("function", schema)
        name = func_def.get("name", "")
        desc = func_def.get("description", "")

        if name.startswith("get_") or name.startswith("list_") or name.startswith("search_"):
            groups["query"].append(schema)
        elif any(name.startswith(p) for p in ("create_", "update_", "submit_", "delete_", "approve_", "reject_")):
            groups["action"].append(schema)
        else:
            groups["other"].append(schema)

    # 如果 other 非空但某组为空，归并到最大的组
    if not groups["query"] and not groups["action"]:
        groups["query"] = tools_schema
        groups["action"] = []
        groups["other"] = []

    return {k: v for k, v in groups.items() if v}
