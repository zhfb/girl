import json
from pathlib import Path
from typing import List, Dict
from datetime import datetime
from dataclasses import dataclass, asdict


@dataclass
class MemoryItem:
    id: str
    content: str
    importance: float
    timestamp: str
    memory_type: str

    def to_dict(self) -> Dict:
        return asdict(self)


class LongTermMemory:
    def __init__(self, storage_path: Path):
        self.storage_path = storage_path
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.memories_file = self.storage_path / "memories.json"
        self.memories: List[MemoryItem] = []
        self.load_memories()

    def load_memories(self):
        if self.memories_file.exists():
            try:
                with open(self.memories_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.memories = [MemoryItem(**item) for item in data]
            except Exception:
                self.memories = []

    def save_memories(self):
        with open(self.memories_file, "w", encoding="utf-8") as f:
            json.dump([m.to_dict() for m in self.memories], f, ensure_ascii=False, indent=2)

    def add_memory(self, content: str, importance: float = 0.5, memory_type: str = "general"):
        import uuid
        memory = MemoryItem(
            id=str(uuid.uuid4()),
            content=content,
            importance=importance,
            timestamp=datetime.now().isoformat(),
            memory_type=memory_type
        )
        self.memories.append(memory)
        self.save_memories()

    def get_memories(self, limit: int = 10, memory_type: str = None) -> List[MemoryItem]:
        filtered = self.memories
        if memory_type:
            filtered = [m for m in filtered if m.memory_type == memory_type]
        filtered.sort(key=lambda x: x.importance, reverse=True)
        return filtered[:limit]

    def search_memories(self, query: str, limit: int = 5) -> List[MemoryItem]:
        results = []
        query_lower = query.lower()
        for memory in self.memories:
            if query_lower in memory.content.lower():
                results.append(memory)
        results.sort(key=lambda x: x.importance, reverse=True)
        return results[:limit]

    def delete_memory(self, memory_id: str):
        self.memories = [m for m in self.memories if m.id != memory_id]
        self.save_memories()

    def clear(self):
        self.memories = []
        self.save_memories()
