from .minimax import MiniMax
from .qwen import Qwen
from .spark import Spark
from .wenxin import ERNIEBot
from .zhipu import Zhipu
from .gpt import GPT
from .config import settings
from .base import LLM, ChatInput, ChatOutput

# Define a dictionary to map model names to their respective classes and settings
MODEL_MAP = {
    "gpt": {
        "models": [
            "gpt-4-0125-preview",
            "gpt-4-turbo-preview",
            "gpt-4-1106-preview",
            "gpt-4",
            "gpt-4-0613",
            "gpt-4-32k",
            "gpt-4-32k-0613",
            "gpt-3.5-turbo-0125",
            "gpt-3.5-turbo",
            "gpt-3.5-turbo-1106",
            "gpt-3.5-turbo-instruct",
        ],
        "class": GPT,
        "settings": ["openai_api_key"],
    },
    "minimax": {
        "models": ["abab6-chat", "abab5.5-chat", "abab5.5s-chat"],
        "class": MiniMax,
        "settings": ["minimax_group_id", "minimax_secret_key"],
    },
    "qwen": {
        "models": [
            "qwen-max",
            "qwen-turbo",
            "qwen-plus",
            "qwen-max-1201",
            "qwen-max-longcontext",
        ],
        "class": Qwen,
        "settings": ["qwen_api_key"],
    },
    "spark": {
        "models": ["spark"],
        "class": Spark,
        "settings": ["spark_app_id", "spark_api_key", "spark_api_secret"],
    },
    "ernie": {
        "models": [
            "ERNIE-Bot-4",
            "ERNIE-Bot-8k",
            "ERNIE-Bot",
            "ERNIE-3.5-4K-0205",
            "ERNIE-3.5-8K-0205",
            "ERNIE-3.5-8K-1222",
            "ERNIE-Bot-turbo",
        ],
        "class": ERNIEBot,
        "settings": ["wenxin_api_key", "wenxin_secret_key"],
    },
    "zhipu": {
        "models": ["glm-4", "glm-3-turbo"],
        "class": Zhipu,
        "settings": ["zhipu_api_key"],
    },
}


def create_model_instance(model_name) -> LLM:
    for model_type, model_info in MODEL_MAP.items():
        if model_name in model_info["models"]:
            model_class = model_info["class"]
            model_settings = {
                setting: getattr(settings, setting) for setting in model_info["settings"]
            }
            return model_class(**model_settings, model_name=model_name)

    raise ValueError(f"model_name: {model_name} is not supported.")


def call_llm(model_name: str, **kwargs) -> ChatOutput:
    llm = create_model_instance(model_name)
    return llm.chat(ChatInput(**kwargs))
