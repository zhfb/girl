from abc import ABC, abstractmethod
from typing import List, Dict, AsyncGenerator, Union


class LLMAdapter(ABC):
    def __init__(self, config: Dict):
        self.config = config

    @abstractmethod
    async def chat(
        self,
        messages: List[Dict[str, str]],
        stream: bool = False
    ) -> Union[AsyncGenerator[str, None], str]:
        pass


class TTSAdapter(ABC):
    def __init__(self, config: Dict):
        self.config = config

    @abstractmethod
    async def synthesize(self, text: str, output_path: str) -> str:
        pass
