from .base import LLMAdapter, TTSAdapter
from .llm import DeepSeekAdapter, OpenAIAdapter
from .tts import EdgeTTSAdapter


def get_llm_adapter(model_type: str, config: dict) -> LLMAdapter:
    adapters = {
        "deepseek": DeepSeekAdapter,
        "openai": OpenAIAdapter
    }
    adapter_class = adapters.get(model_type)
    if not adapter_class:
        raise ValueError(f"Unsupported LLM model type: {model_type}")
    return adapter_class(config)


def get_tts_adapter(model_type: str, config: dict) -> TTSAdapter:
    adapters = {
        "edge-tts": EdgeTTSAdapter
    }
    adapter_class = adapters.get(model_type)
    if not adapter_class:
        raise ValueError(f"Unsupported TTS model type: {model_type}")
    return adapter_class(config)


__all__ = [
    "LLMAdapter",
    "TTSAdapter",
    "DeepSeekAdapter",
    "OpenAIAdapter",
    "EdgeTTSAdapter",
    "get_llm_adapter",
    "get_tts_adapter"
]
