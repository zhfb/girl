import asyncio
import edge_tts
from typing import Dict
from ..base import TTSAdapter


class EdgeTTSAdapter(TTSAdapter):
    def __init__(self, config: Dict):
        super().__init__(config)
        self.voice = config.get("voice", "zh-CN-XiaoxiaoNeural")
        self.rate = config.get("rate", "+0%")
        self.pitch = config.get("pitch", "+0Hz")

    async def synthesize(self, text: str, output_path: str) -> str:
        communicate = edge_tts.Communicate(
            text=text,
            voice=self.voice,
            rate=self.rate,
            pitch=self.pitch
        )
        await communicate.save(output_path)
        return output_path
