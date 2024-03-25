from sparkdesk_api.core import SparkAPI
from .base import LLM, ChatInput, ChatOutput


class Spark(LLM):
    def __init__(self, spark_app_id: str, spark_api_key: str, spark_api_secret: str, model_name: str) -> None:
        super().__init__(model_name)
        self.__spark_app_id = spark_app_id
        self.__spark_api_secret = spark_api_secret
        self.__spark_api_key = spark_api_key

        # 默认api接口版本为3.1，配置其他版本需要指定Version参数（2.1或者1.1）
        self.sparkAPI = SparkAPI(
            app_id=self.__spark_app_id,
            api_secret=self.__spark_api_secret,
            api_key=self.__spark_api_key,
        )

    def chat(self, chat_input: ChatInput):
        response = self.sparkAPI.chat(
            query=chat_input.prompt,
            max_tokens=chat_input.max_tokens,
            temperature=chat_input.temperature,
        )

        return ChatOutput(response=response)
