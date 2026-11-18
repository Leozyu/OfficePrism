import asyncio
from typing import Any, List, Optional, Dict

from loguru import logger
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from configs.config_loader import config, Config


def run_async(coro):
    """
    在同步环境（含 Jupyter）中安全运行异步协程。
    自动判断当前是否已有运行中的事件循环。
    """
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    if loop.is_running():
        future = asyncio.ensure_future(coro)
        return future.result() if hasattr(future, "result") else asyncio.run(coro)
    else:
        return loop.run_until_complete(coro)


class LLMClient:
    """
    ChatOpenAI 的同步/异步封装，支持并发控制和流式输出。

    Args:
        model_name: 模型名称，默认读取 config.llm.model_name
    """
    def __init__(self, model_name: Optional[str] = None, max_tokens: Optional[int] = None, new_config: Optional[Config] = None) -> None:
        self.config = new_config or config
        self.llm = ChatOpenAI(
            model=model_name or self.config.llm.model_name,
            api_key=self.config.llm.api_key,
            base_url=self.config.llm.base_url,
            temperature=self.config.llm.temperature,
            max_tokens=max_tokens or self.config.llm.max_tokens,
            timeout=self.config.llm.get("timeout", 600),
            streaming=True,
            stream_options={"include_usage": True},
        )
        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small",
            api_key=self.config.llm.api_key,
            base_url=self.config.llm.base_url,
            timeout=self.config.llm.get("timeout", 600),
        )
        self._sem = asyncio.Semaphore(self.config.llm.max_concurrent)

    def generate(self, message: str, return_raw: bool = False) -> Any:
        res = self.llm.invoke([{"role": "user", "content": message}])
        return res if return_raw else res.content

    async def generate_async(self, message: str) -> Any:
        async with self._sem:
            try:
                return await self.llm.ainvoke([{"role": "user", "content": message}])
            except Exception as e:
                logger.error(f"Error generating: {e}")
                return f"Error generating: {str(e)}, failed calling llm."

    def generate_batch(self, messages: List[str]) -> List[Any]:
        return run_async(self._generate_batch_async(messages))

    async def _generate_batch_async(self, messages: List[str]) -> List[Any]:
        tasks = [self.generate_async(m) for m in messages]
        return await asyncio.gather(*tasks)

    def get_embedding(self, text: str) -> List[float]:
        return self.embeddings.embed_query(text)

    def get_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        return self.embeddings.embed_documents(texts)

    def generate_from_template(
        self, template_path: str, variables: Dict[str, Any],
        system_prompt: str = "You are a helpful AI assistant."
    ) -> str:
        """从模板文件读取并替换 {{key}} 占位符后调用 LLM"""
        with open(template_path, 'r', encoding='utf-8') as f:
            template = f.read()
        for key, value in variables.items():
            template = template.replace(f"{{{{{key}}}}}", str(value))
        return self.generate(template)


if __name__ == "__main__":
    client = LLMClient()
    msgs = ["hello", "what is java", "what is c++"]
    results = client.generate_batch(msgs)
    for r in results:
        logger.info(r.content)
