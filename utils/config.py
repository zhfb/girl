import json
import os
from pathlib import Path


class ConfigManager:
    def __init__(self):
        self.config = {}
        self.config_dir = self.get_config_dir()
        self.config_path = self.config_dir / "config.json"
        self.load_config()

    @staticmethod
    def get_config_dir():
        app_name = "AIGirlfriend"
        if os.name == "nt":
            base_dir = Path(os.environ["APPDATA"])
        elif os.name == "posix":
            if "HOME" in os.environ:
                base_dir = Path(os.environ["HOME"])
                if os.uname().sysname == "Darwin":
                    base_dir = base_dir / "Library" / "Application Support"
                else:
                    base_dir = base_dir / ".config"
            else:
                base_dir = Path.cwd()
        else:
            base_dir = Path.cwd()
        
        config_dir = base_dir / app_name
        config_dir.mkdir(parents=True, exist_ok=True)
        return config_dir

    def get_data_dir(self, subdir=None):
        data_dir = self.config_dir
        if subdir:
            data_dir = data_dir / subdir
            data_dir.mkdir(parents=True, exist_ok=True)
        return data_dir

    def load_config(self):
        if self.config_path.exists():
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    self.config = json.load(f)
            except Exception:
                self.config = self.get_default_config()
        else:
            self.config = self.get_default_config()
            self.save_config()

    def save_config(self):
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)

    def get_default_config(self):
        return {
            "active_llm": "deepseek",
            "active_tts": "edge-tts",
            "llm_models": {
                "deepseek": {
                    "api_key": "",
                    "api_base": "https://api.deepseek.com",
                    "model": "deepseek-chat",
                    "temperature": 0.7,
                    "max_tokens": 2000
                },
                "openai": {
                    "api_key": "",
                    "api_base": "https://api.openai.com/v1",
                    "model": "gpt-3.5-turbo",
                    "temperature": 0.7
                }
            },
            "tts_models": {
                "edge-tts": {
                    "voice": "zh-CN-XiaoxiaoNeural",
                    "rate": "+0%",
                    "pitch": "+0Hz"
                }
            },
            "character": {
                "name": "小萌",
                "nickname": "萌萌",
                "personality": ["温柔", "可爱", "体贴"],
                "avatar": "default",
                "background_story": "你的大学学妹，性格温柔善良，喜欢看书和听音乐。"
            },
            "memory": {
                "short_term_max": 20,
                "long_term_enabled": True,
                "auto_summarize": True
            }
        }

    def get(self, key, default=None):
        keys = key.split(".")
        value = self.config
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value

    def set(self, key, value):
        keys = key.split(".")
        config = self.config
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value
        self.save_config()
