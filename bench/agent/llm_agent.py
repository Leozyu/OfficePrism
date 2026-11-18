# 此文件保留向后兼容导入。
# Dialog 模式的 LLMAgent / LLMGTAgent / LLMSoloAgent 已归档至 backup/dialog_agents/。
# 主要 Agent 实现见：react_agent.py, function_calling_agent.py, plan_execute_agent.py

from bench.agent.react_agent import ReActAgent
from bench.agent.react_agent import ReActAgent as ReActSoloAgent  # 向后兼容
