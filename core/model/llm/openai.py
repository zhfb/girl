import aiohttp
from typing import List, Dict, AsyncGenerator
from ..base import LLMAdapter


class OpenAIAdapter(LLMAdapter):
    def __init__(self, config: Dict):
        super().__init__(config)
        self.api_key = config.get("api_key", "")
        self.api_base = config.get("api_base", "https://api.openai.com/v1")
        self.model = config.get("model", "gpt-3.5-turbo")
        self.temperature = config.get("temperature", 0.7)
        self.max_tokens = config.get("max_tokens", 2000)

    async def chat(
        self,
        messages: List[Dict[str, str]],
        stream: bool = False
    ) -> AsyncGenerator[str, None] | str:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature,
            "stream": stream
        }
        if self.max_tokens:
            payload["max_tokens"] = self.max_tokens

        if stream:
            return self._chat_stream(headers, payload)
        else:
            return await self._chat_non_stream(headers, payload)

    async def _chat_stream(self, headers: Dict, payload: Dict) -> AsyncGenerator[str, None]:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.api_base}/chat/completions",
                headers=headers,
                json=payload
            ) as response:
                async for line in response.content:
                    line = line.decode("utf-8").strip()
                    if line.startswith("data: "):
                        data = line[6:]
                        if data == "[DONE]":
                            break
                        import json
                        try:
                            chunk = json.loads(data)
                            if "choices" in chunk and len(chunk["choices"]) > 0:
                                delta = chunk["choices"][0].get("delta", {})
                                content = delta.get("content", "")
                                if content:
                                    yield content
                        except Exception:
                            pass

    async def _chat_non_stream(self, headers: Dict, payload: Dict) -> str:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.api_base}/chat/completions",
                headers=headers,
                json=payload
            ) as response:
                data = await response.json()
                if "choices" in data and len(data["choices"]) > 0:
                    return data["choices"][0]["message"]["content"]
                return ""
