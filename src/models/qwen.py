import random
import dashscope
from http import HTTPStatus
from .base import LLM, ChatInput, ChatOutput, Message


class Qwen(LLM):
    # documentation: https://help.aliyun.com/zh/dashscope/developer-reference/api-details
    def __init__(self, qwen_api_key: str, model_name: str):
        super().__init__(model_name)
        dashscope.api_key = qwen_api_key

    def chat(self, chat_input: ChatInput):
        messages = [
            Message(role="system", content="You are a helpful assistant."),
            Message(role="user", content=chat_input.prompt),
        ]

        response = dashscope.Generation.call(
            model=self.model_name,  # qwen-turbo; qwen-plus
            messages=messages,
            top_p=chat_input.top_p,
            temperature=chat_input.temperature,
            max_tokens=chat_input.max_tokens,
            seed=random.randint(1, 10000),
            result_format="message",
            enable_search=False,
        )
        if response.status_code == HTTPStatus.OK:
            return ChatOutput(
                response=response["output"]["choices"][0]["message"]["content"]
            )
        else:
            print(
                "Request id: %s, Status code: %s, error code: %s, error message: %s"
                % (
                    response.request_id,
                    response.status_code,
                    response.code,
                    response.message,
                )
            )
