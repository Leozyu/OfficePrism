import json
import re
import uuid
import time
from typing import Any, Optional, Tuple
from loguru import logger
import openai

from bench.config import DEFAULT_MAX_RETRIES
from bench.data_model.message import (
    AssistantMessage,
    Message,
    SystemMessage,
    ToolCall,
    ToolMessage,
    UserMessage,
)
from bench.environment.tool import Tool


_TASK_JSON_KEYS = (
    "business_scenario",
    "reasoning",
    "question",
    "answer",
    "final_answer",
)


def _try_parse_truncated_json(candidate: str) -> Any:
    """尝试修复被截断的 JSON 片段（补齐引号/括号后再解析）。"""
    text = candidate.strip().rstrip("`")
    if not text:
        return None

    obj_start = text.find("{")
    arr_start = text.find("[")
    if obj_start == -1 and arr_start == -1:
        return None

    if obj_start == -1:
        start = arr_start
    elif arr_start == -1:
        start = obj_start
    else:
        start = min(obj_start, arr_start)

    text = text[start:].strip()

    # 若字符串未闭合，先补一个引号，避免 json.loads 直接失败
    if text.count('"') % 2 == 1:
        text += '"'

    brace_diff = text.count("{") - text.count("}")
    if brace_diff > 0:
        text += "}" * brace_diff

    bracket_diff = text.count("[") - text.count("]")
    if bracket_diff > 0:
        text += "]" * bracket_diff

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None


def _extract_task_fields_fallback(candidate: str) -> Optional[dict[str, str]]:
    """按既定字段顺序提取字符串值，兼容 value 内未转义双引号。"""
    recovered: dict[str, str] = {}
    for idx, key in enumerate(_TASK_JSON_KEYS):
        next_keys = _TASK_JSON_KEYS[idx + 1 :]
        next_part = "|".join(re.escape(k) for k in next_keys)
        if next_part:
            pattern = (
                rf'"{re.escape(key)}"\s*:\s*"([\s\S]*?)"\s*'
                rf'(?=,\s*"(?:{next_part})"\s*:|\s*\}}|\s*$)'
            )
        else:
            pattern = rf'"{re.escape(key)}"\s*:\s*"([\s\S]*?)"\s*(?=\s*\}}|\s*$)'
        match = re.search(pattern, candidate)
        if not match:
            continue
        recovered[key] = match.group(1).strip()

    if not recovered:
        return None
    return {key: recovered.get(key, "") for key in _TASK_JSON_KEYS}


def extract_json_from_llm_response(text: str) -> Any:
    """
    从 LLM 原始文本中提取并解析 JSON（对象或数组）。
    """
    if not isinstance(text, str):
        raise ValueError("LLM 输出不是字符串，无法解析 JSON")

    raw = text.strip()
    if not raw:
        raise ValueError("LLM 输出为空，无法解析 JSON")

    # 兼容 ```json ... ``` / ``` ... ``` 包裹
    code_block = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", raw, re.IGNORECASE)
    candidate = code_block.group(1).strip() if code_block else raw

    # 兼容未闭合代码块：```json 开头但被截断，没有尾部 ```
    if not code_block:
        open_code_block = re.search(r"```(?:json)?\s*([\s\S]*)$", raw, re.IGNORECASE)
        if open_code_block:
            candidate = open_code_block.group(1).strip()

    # 优先直解析，成功直接返回
    try:
        return json.loads(candidate)
    except json.JSONDecodeError:
        pass

    # 回退：提取第一个 JSON 对象
    obj_match = re.search(r"\{[\s\S]*\}", candidate)
    if obj_match:
        try:
            return json.loads(obj_match.group(0))
        except json.JSONDecodeError:
            pass

    # 回退：提取第一个 JSON 数组
    arr_match = re.search(r"\[[\s\S]*\]", candidate)
    if arr_match:
        try:
            return json.loads(arr_match.group(0))
        except json.JSONDecodeError:
            pass

    # 回退：截断修复（补齐引号/括号）
    repaired = _try_parse_truncated_json(candidate)
    if repaired is not None:
        return repaired

    # 回退：任务字段兜底提取（兼容 value 内未转义双引号）
    fallback_obj = _extract_task_fields_fallback(candidate)
    if fallback_obj is not None:
        return fallback_obj

    raise ValueError(f"无法从 LLM 输出中解析 JSON：{raw[:500]}")


def to_openai_messages(messages: list[Message]) -> list[dict]:
    """
    Convert a list of Tau2 messages to a list of OpenAI messages.
    """
    openai_messages = []
    for message in messages:
        if isinstance(message, UserMessage):
            openai_messages.append({"role": "user", "content": message.content})
        elif isinstance(message, AssistantMessage):
            tool_calls = None
            if message.is_tool_call():
                tool_calls = [
                    {
                        "id": tc.id,
                        "function": {
                            "name": tc.name,
                            "arguments": json.dumps(tc.arguments) if not isinstance(tc.arguments, str) else tc.arguments,
                        },
                        "type": "function",
                    }
                    for tc in message.tool_calls
                ]
            openai_messages.append(
                {
                    "role": "assistant",
                    "content": message.content,
                    "tool_calls": tool_calls,
                }
            )
            # OpenAI doesn't like null/None values for tool_calls if empty, just omit them
            if not tool_calls:
                openai_messages[-1].pop("tool_calls")
        elif isinstance(message, ToolMessage):
            openai_messages.append(
                {
                    "role": "tool",
                    "content": message.content,
                    "tool_call_id": message.id,
                }
            )
        elif isinstance(message, SystemMessage):
            openai_messages.append({"role": "system", "content": message.content})
    return openai_messages


def _collect_chat_stream(
    client: openai.OpenAI, req_kwargs: dict[str, Any]
) -> Tuple[str, Optional[dict]]:
    """
    流式消费 chat completion，拼接文本；部分网关会在末包附带 usage。
    长文本生成时持续有字节到达，有利于避免「等整包」触发的读超时。
    """
    req_kwargs = {**req_kwargs, "stream": True}
    stream = client.chat.completions.create(**req_kwargs)
    parts: list[str] = []
    usage_dict: Optional[dict] = None
    for i, chunk in enumerate(stream):
        u = getattr(chunk, "usage", None)
        if u is not None:
            usage_dict = {
                "prompt_tokens": u.prompt_tokens,
                "completion_tokens": u.completion_tokens,
                "total_tokens": u.total_tokens,
            }
            logger.debug("[LLM stream] chunk #{} usage: {}", i, usage_dict)
        if not chunk.choices:
            continue
        delta = chunk.choices[0].delta
        if delta is None or not delta.content:
            continue
        logger.debug("[LLM stream] chunk #{}: {!r}", i, delta.content)
        parts.append(delta.content)
    return "".join(parts), usage_dict


def _model_unsupported_params(model_id: str, llm_config: dict) -> set[str]:
    """按模型/端点类型返回应从请求中剔除的参数名。

    在发请求前就决定带哪些参数，避免每次调用都靠 400 试错。
    可用 llm_config["unsupported_params"] 显式追加/覆盖。
    - enable_thinking：仅 dashscope 兼容端点支持（qwen/deepseek/glm 均可）；
      其它网关（如 网关）不认，一律剔除。按端点而非模型名区分，避免误伤国产模型。
    - temperature：claude 系与 gpt-5 / o 系推理模型（网关 转原生协议）拒收自定义值。
    """
    ml = (model_id or "").lower()
    base_url = (llm_config.get("base_url") or "").lower()
    dropped = set(llm_config.get("unsupported_params") or [])
    if "dashscope" not in base_url and "aliyuncs" not in base_url:
        dropped.add("enable_thinking")
    if any(k in ml for k in ("claude", "opus", "sonnet", "haiku")) or ml.startswith(
        ("gpt-5", "o1", "o3", "o4")
    ):
        dropped.add("temperature")
    return dropped


def generate(
    model: str,
    messages: list[Message],
    tools: Optional[list[Tool]] = None,
    tool_choice: Optional[str] = None,
    debug: bool = False,
    llm_config: Optional[dict] = None,
    stream: bool = False,
    **kwargs: Any,
) -> AssistantMessage:
    """
    Generate a response from the model using the standard OpenAI client.

    Args:
        model: The model to use.
        messages: The messages to send to the model.
        tools: The tools to use.
        tool_choice: The tool choice to use.
        llm_config: LLM configuration dict (base_url, api_key, timeout, etc.).
        stream: 为 True 时使用流式输出（仅无 tools；与 tools 并存会回退非流式）。流式时各 chunk 打 logger.debug，需日志级别含 DEBUG。
        **kwargs: Additional arguments to pass to the model.

    Returns: AssistantMessage containing the generated response or tool calls.
    """
    if llm_config is None:
        llm_config = {}

    api_key = llm_config.get("api_key") or kwargs.get("api_key") or "dummy"
    base_url = llm_config.get("base_url") or kwargs.get("base_url")
    timeout = llm_config.get("timeout", kwargs.get("timeout", 600.0))
    if isinstance(timeout, (int, float)):
        timeout_val: Any = float(timeout)
    else:
        timeout_val = 600.0

    client = openai.OpenAI(
        api_key=api_key,
        base_url=base_url,
        timeout=timeout_val,
    )

    openai_messages = to_openai_messages(messages)
    openai_tools = [tool.openai_schema for tool in tools] if tools else None

    if openai_tools and tool_choice is None:
        tool_choice = "auto"

    if stream and openai_tools:
        logger.warning("generate(stream=True) 与 tools 并存时回退为非流式")
        stream = False

    num_retries = kwargs.get("num_retries", DEFAULT_MAX_RETRIES)
    temperature = llm_config.get("temperature", kwargs.get("temperature", 0.7))
    max_tokens = llm_config.get("max_tokens", kwargs.get("max_tokens", 4000))
    extra_body = llm_config.get("extra_body")
    if "enable_thinking" in llm_config:
        extra_body = dict(extra_body or {})
        extra_body["enable_thinking"] = llm_config["enable_thinking"]

    response = None
    last_error = None
    # 按模型类型预先决定不支持的采样参数（temperature / enable_thinking 等），
    # 首次请求就不带，避免每步都靠 400 试错。运行时自动剔除仅作未知参数兜底。
    drop_params: set[str] = _model_unsupported_params(
        str(llm_config.get("model", model) or ""), llm_config
    )

    attempt = 0
    while attempt < num_retries:
        try:
            req_kwargs = {
                "model": llm_config.get("model", model),
                "messages": openai_messages,
                "max_tokens": max_tokens,
            }
            if "temperature" not in drop_params:
                req_kwargs["temperature"] = temperature
            if extra_body:
                filtered_extra = {k: v for k, v in extra_body.items() if k not in drop_params}
                if filtered_extra:
                    req_kwargs["extra_body"] = filtered_extra
            if openai_tools:
                req_kwargs["tools"] = openai_tools
                req_kwargs["tool_choice"] = tool_choice

            if stream and not openai_tools:
                content, usage_dict = _collect_chat_stream(client, req_kwargs)
                return AssistantMessage(
                    role="assistant",
                    content=content,
                    tool_calls=None,
                    usage=usage_dict,
                    raw_data={"stream": True},
                )

            response = client.chat.completions.create(**req_kwargs)
            break
        except Exception as e:
            msg = str(e)
            # 新模型（网关 上的 claude/gpt-5 系）会拒收 qwen 专有或已弃用的采样参数，
            # 命中错误信息里的参数名就去掉它立即重试，无需为每个模型单独配置。
            _optional = ("temperature", "top_p", "enable_thinking")
            newly = [p for p in _optional if p in msg and p not in drop_params]
            if newly:
                logger.warning(f"模型拒绝参数 {newly}，去掉后立即重试")
                drop_params.update(newly)
                continue  # 参数剔除不计入重试预算，直接重试
            # thinking 模式模型（如 网关 上的 qwen4-max）不支持 tool_choice=required/object：
            # "The tool_choice parameter does not support being set to required or object in thinking mode"。
            # 命中即把 tool_choice 降级为 auto 立即重试（不计入重试预算），无需为每个模型单独配置。
            if (
                openai_tools
                and tool_choice not in (None, "auto")
                and "tool_choice" in msg
                and ("thinking mode" in msg or "required or object" in msg)
            ):
                logger.warning("模型不支持 tool_choice=required（thinking 模式），降级为 auto 重试")
                tool_choice = "auto"
                continue
            attempt += 1
            logger.error(f"API call error: {e}")
            last_error = e
            time.sleep(5)

    if response is None:
        logger.error("Failed to get response after retries.")
        # Return a fallback or raise depending on preference, let's return error message
        return AssistantMessage(
            role="assistant",
            content=f"Error: {str(last_error)}",
            tool_calls=None
        )

    finish_reason = response.choices[0].finish_reason
    if finish_reason == "length":
        logger.warning("LLM 输出触发长度截断（finish_reason=length），内容可能不完整")

    response_message = response.choices[0].message
    content = response_message.content

    tool_calls = []
    if response_message.tool_calls:
        for tc in response_message.tool_calls:
            try:
                args = json.loads(tc.function.arguments)
            except json.JSONDecodeError:
                args = tc.function.arguments  # Fallback to string if invalid JSON
            
            tool_calls.append(
                ToolCall(
                    id=tc.id or str(uuid.uuid4()),
                    name=tc.function.name,
                    arguments=args,
                )
            )

    usage_dict = None
    if hasattr(response, "usage") and response.usage:
        usage_dict = {
            "prompt_tokens": response.usage.prompt_tokens,
            "completion_tokens": response.usage.completion_tokens,
            "total_tokens": response.usage.total_tokens,
        }

    raw_data = response.model_dump()
    if isinstance(raw_data, dict):
        raw_data["_finish_reason"] = finish_reason

    message = AssistantMessage(
        role="assistant",
        content=content,
        tool_calls=tool_calls if tool_calls else None,
        usage=usage_dict,
        raw_data=raw_data,
    )
    return message


def get_cost(messages: list[Message]) -> tuple[float, float] | None:
    """基于 usage tokens 统计 agent/user 消耗，无 usage 时返回 (0, 0) 而非 None。"""
    agent_cost = 0.0
    user_cost = 0.0
    for message in messages:
        if isinstance(message, ToolMessage):
            continue
        if message.cost is not None:
            if isinstance(message, AssistantMessage):
                agent_cost += message.cost
            elif isinstance(message, UserMessage):
                user_cost += message.cost
    return agent_cost, user_cost


def get_token_usage(messages: list[Message]) -> dict:
    """
    Get the token usage of the interaction between the agent and the user.
    """
    usage = {"completion_tokens": 0, "prompt_tokens": 0}
    for message in messages:
        if isinstance(message, ToolMessage):
            continue
        if message.usage is None:
            continue
        usage["completion_tokens"] += message.usage.get("completion_tokens", 0)
        usage["prompt_tokens"] += message.usage.get("prompt_tokens", 0)
    return usage
