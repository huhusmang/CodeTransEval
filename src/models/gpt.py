from openai import OpenAI
from .base import LLM, ChatInput, ChatOutput, Message


class GPT(LLM):
    def __init__(self, openai_api_key: str, model_name: str) -> None:
        super().__init__(model_name)
        self.__openai_api_key = openai_api_key

    def chat(self, chat_input: ChatInput):
        """
        Generate a chat response.

        :param chat_input: The input for the chat
        :return: The chat response
        """
        base_url = "https://gptmos.com/v1"
        client = OpenAI(api_key=self.__openai_api_key, base_url=base_url)

        response = client.chat.completions.create(
            model=self.model_name,
            messages=[Message(role="user", content=chat_input.prompt).model_dump()],
            max_tokens=chat_input.max_tokens,
            temperature=chat_input.temperature,
            seed=1239,
        )
        outputs = response.choices[0].message.content

        return ChatOutput(response=outputs)
