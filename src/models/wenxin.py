import qianfan
from .base import LLM, ChatInput, ChatOutput, Message


class ERNIEBot(LLM):
    # document: https://cloud.baidu.com/doc/WENXINWORKSHOP/s/xlmokikxe
    def __init__(self, wenxin_api_key: str, wenxin_secret_key: str, model_name: str):
        super().__init__(model_name)
        self.__wenxin_api_key = wenxin_api_key
        self.__wenxin_secret_key = wenxin_secret_key

    def chat(self, chat_input: ChatInput):
        chat_comp = qianfan.ChatCompletion(ak=self.__wenxin_api_key, sk=self.__wenxin_secret_key)

        resp = chat_comp.do(
            model=self.model_name,
            messages=[
                Message(role="user", content=chat_input.prompt).model_dump()
            ],
            top_p=chat_input.top_p,
            temperature=chat_input.temperature,
            max_output_tokens=chat_input.max_tokens,
        )

        if resp["finish_reason"] == "normal" and len(resp["result"]) > 0:
            return ChatOutput(response=resp["result"])
