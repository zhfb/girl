import asyncio
import json
from pathlib import Path
from typing import List, Dict, AsyncGenerator, Optional
from datetime import datetime

from ..model import get_llm_adapter, get_tts_adapter, LLMAdapter, TTSAdapter
from ..memory import ShortTermMemory, LongTermMemory
from ..prompt import get_prompt_builder, PromptTemplate
from utils import ConfigManager


class ChatManager:
    def __init__(self, config_manager: ConfigManager):
        self.config = config_manager
        self.short_term_memory = ShortTermMemory(
            max_messages=self.config.get("memory.short_term_max", 20)
        )
        self.long_term_memory = LongTermMemory(
            storage_path=self.config.get_data_dir("memories")
        )
        self.chat_history_path = self.config.get_data_dir("chat_history")
        self.current_llm_adapter: Optional[LLMAdapter] = None
        self.current_tts_adapter: Optional[TTSAdapter] = None
        self._init_adapters()
        self._load_chat_history()

    def _init_adapters(self):
        active_llm = self.config.get("active_llm", "deepseek")
        llm_config = self.config.get(f"llm_models.{active_llm}", {})
        if llm_config:
            self.current_llm_adapter = get_llm_adapter(active_llm, llm_config)

        active_tts = self.config.get("active_tts", "edge-tts")
        tts_config = self.config.get(f"tts_models.{active_tts}", {})
        if tts_config:
            self.current_tts_adapter = get_tts_adapter(active_tts, tts_config)

    def _load_chat_history(self):
        history_file = self.chat_history_path / "current.json"
        if history_file.exists():
            try:
                with open(history_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for msg in data:
                        self.short_term_memory.add_message(msg["role"], msg["content"])
            except Exception:
                pass

    def _save_chat_history(self):
        self.chat_history_path.mkdir(parents=True, exist_ok=True)
        history_file = self.chat_history_path / "current.json"
        messages = self.short_term_memory.get_full_messages()
        with open(history_file, "w", encoding="utf-8") as f:
            json.dump([m.to_dict() for m in messages], f, ensure_ascii=False, indent=2)

    def _build_system_prompt(self) -> str:
        character_config = self.config.get("character", {})
        template = get_prompt_builder(character_config)
        
        personality = character_config.get("personality", [])
        personality_desc = "、".join(personality) if personality else "温柔可爱"
        
        return template.render(
            name=character_config.get("name", "小萌"),
            personality_desc=personality_desc,
            background_story=character_config.get("background_story", "")
        )

    def _build_messages(self, user_message: str) -> List[Dict[str, str]]:
        system_prompt = self._build_system_prompt()
        messages = [{"role": "system", "content": system_prompt}]
        
        memories = self.long_term_memory.search_memories(user_message, limit=3)
        if memories:
            memory_content = "\n".join([f"- {m.content}" for m in memories])
            messages.append({
                "role": "system",
                "content": f"关于用户的重要信息：\n{memory_content}"
            })
        
        messages.extend(self.short_term_memory.get_messages())
        messages.append({"role": "user", "content": user_message})
        
        return messages

    async def send_message(self, user_message: str, stream: bool = True) -> AsyncGenerator[str, None]:
        self.short_term_memory.add_message("user", user_message)
        
        messages = self._build_messages(user_message)
        
        if not self.current_llm_adapter:
            yield "请先在设置中配置API密钥"
            return
        
        full_response = ""
        try:
            if stream:
                async for chunk in await self.current_llm_adapter.chat(messages, stream=True):
                    full_response += chunk
                    yield chunk
            else:
                full_response = await self.current_llm_adapter.chat(messages, stream=False)
                yield full_response
        except Exception as e:
            yield f"抱歉，发生了错误：{str(e)}"
            return
        
        self.short_term_memory.add_message("assistant", full_response)
        self._save_chat_history()

    async def synthesize_voice(self, text: str) -> Optional[str]:
        if not self.current_tts_adapter:
            return None
        
        voice_dir = self.config.get_data_dir("voices")
        import uuid
        output_path = voice_dir / f"{uuid.uuid4()}.mp3"
        
        try:
            await self.current_tts_adapter.synthesize(text, str(output_path))
            return str(output_path)
        except Exception:
            return None

    def clear_history(self):
        self.short_term_memory.clear()
        self._save_chat_history()

    def reload_config(self):
        self._init_adapters()
        self.short_term_memory.set_max_messages(
            self.config.get("memory.short_term_max", 20)
        )
