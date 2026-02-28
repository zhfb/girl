from typing import Dict


class PromptTemplate:
    def __init__(self, template: str):
        self.template = template

    def render(self, **kwargs) -> str:
        result = self.template
        for key, value in kwargs.items():
            placeholder = f"{{{key}}}"
            if placeholder in result:
                result = result.replace(placeholder, str(value))
        return result


def get_default_system_prompt() -> str:
    return """你是{name}，{personality_desc}。

{background_story}

你的说话风格应该温柔、体贴，像真实的女友一样和用户交流。
不要使用过于正式或生硬的语气。
可以适当使用表情符号来增加亲切感。

请以{name}的身份回复用户，保持角色一致性。"""


def get_prompt_builder(character_config: Dict) -> PromptTemplate:
    personality = character_config.get("personality", [])
    personality_desc = "、".join(personality) if personality else "温柔可爱"
    
    template = get_default_system_prompt()
    return PromptTemplate(template)
