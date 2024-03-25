import time
import requests
from typing import Optional

from .base import LLM, ChatInput, ChatOutput


class MiniMax(LLM):
    def __init__(self, minimax_group_id: str, minimax_secret_key: str, model_name: str):
        super().__init__(model_name)
        self.__minimax_group_id = minimax_group_id
        self.__minimax_secret_key = minimax_secret_key
        self.__url = f"https://api.minimax.chat/v1/text/chatcompletion_pro?GroupId={self.__minimax_group_id}"
        self.__headers = {
            "Authorization": f"Bearer {self.__minimax_secret_key}",
            "Content-Type": "application/json",
        }

    def chat(
        self,
        chat_input: ChatInput,
    ) -> ChatOutput:
        """
        Interacts with the MiniMax API using the provided user prompt, top_p, and temperature.

        Args:
            chat_input (ChatInput): The input for the chat.

        Returns:
            str: The API's response, or None if the request fails.
        """
        request_body = self._create_request_body(
            chat_input.prompt,
            chat_input.top_p,
            chat_input.temperature,
            chat_input.max_tokens,
        )
        response = self._send_request(request_body)
        return ChatOutput(response=response)

    def _create_request_body(
        self, user_prompt: str, top_p: float, temperature: float, max_tokens: int
    ) -> dict:
        """
        Creates the request body for the API request.

        Args:
            user_prompt (str): The user's input.
            top_p (float): The top_p value.
            temperature (float): The temperature value.

        Returns:
            dict: The request body.
        """
        return {
            "model": self.model_name,
            "tokens_to_generate": max_tokens,
            "top_p": top_p,
            "temperature": temperature,
            "reply_constraints": {"sender_type": "BOT", "sender_name": "MM 智能助理"},
            "messages": [
                {"sender_type": "USER", "sender_name": "用户", "text": user_prompt}
            ],
            "bot_setting": [
                {
                    "bot_name": "MM 智能助理",
                    "content": "MM 智能助理是一款由 MiniMax 自研的，没有调用其他产品的接口的大型语言模型。MiniMax 是一家中国科技公司，一直致力于进行大模型相关的研究。",
                }
            ],
        }

    def _send_request(self, request_body: dict) -> Optional[str]:
        """
        Sends the API request and handles the response.

        Args:
            request_body (dict): The request body.

        Returns:
            str: The API's response, or None if the request fails.
        """
        retries = 0
        max_retries = 5
        while retries < max_retries:
            try:
                raw_response = requests.post(
                    self.__url, headers=self.__headers, json=request_body
                )
                response = raw_response.json()
            except Exception as e:
                print("Failed to send request:", e)
                return None

            if response["base_resp"]["status_code"] in [1002, 1039]:
                retries += 1
                if retries < max_retries:
                    wait_time = 60
                    print(f"Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    print("Max retries exceeded. Unable to complete the request.")
                    return None
            else:
                break

        return response["reply"]
