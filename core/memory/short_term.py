from collections import deque
from typing import List, Dict
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ChatMessage:
    role: str
    content: str
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

    def to_dict(self) -> Dict:
        return {
            "role": self.role,
            "content": self.content,
            "timestamp": self.timestamp.isoformat()
        }


class ShortTermMemory:
    def __init__(self, max_messages: int = 20):
        self.max_messages = max_messages
        self.messages: deque = deque(maxlen=max_messages)

    def add_message(self, role: str, content: str):
        self.messages.append(ChatMessage(role=role, content=content))

    def get_messages(self) -> List[Dict[str, str]]:
        return [{"role": m.role, "content": m.content} for m in self.messages]

    def get_full_messages(self) -> List[ChatMessage]:
        return list(self.messages)

    def clear(self):
        self.messages.clear()

    def set_max_messages(self, max_messages: int):
        self.max_messages = max_messages
        self.messages = deque(self.messages, maxlen=max_messages)
