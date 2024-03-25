from zhipuai import ZhipuAI
from .base import LLM, ChatInput, ChatOutput, Message


class Zhipu(LLM):
    # document: https://open.bigmodel.cn/dev/api#overview
    def __init__(self, zhipu_api_key: str, model_name: str):
        super().__init__(model_name)
        self.__zhipu_api_key = zhipu_api_key

    def chat(self, chat_input: ChatInput):
        client = ZhipuAI(api_key=self.__zhipu_api_key)
        response = client.chat.completions.create(
            model=self.model_name,
            messages=[Message(role="user", content=chat_input.prompt).model_dump()],
            top_p=chat_input.top_p,
            temperature=chat_input.temperature,
            max_tokens=chat_input.max_tokens,
        )

        if response["choices"][0]["finish_reason"] != "stop":
            print(f"Failed to get response for prompt: {chat_input.user_prompt}")
            print(response)
        else:
            result = response["choices"][0]["message"]["content"]
            return ChatOutput(response=result)
