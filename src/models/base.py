from abc import ABC, abstractmethod
from pydantic import BaseModel


class ChatInput(BaseModel):
    prompt: str
    top_p: float = 0.7
    temperature: float = 0.9
    max_tokens: int = 3000


class ChatOutput(BaseModel):
    response: str


class Message(BaseModel):
    """
    Message class for chat input.

    Attributes:
        role (str): Role of the message sender.
        content (str): Content of the message.
    """

    role: str
    content: str


class LLM(ABC):
    """Abstract base class for large language models (LLMs)."""

    def __init__(self, model_name: str):
        self.model_name = model_name

    @abstractmethod
    def chat(self, chat_input: ChatInput) -> ChatOutput:
        """Interacts with the LLM using the provided prompt and parameters.

        Args:
            chat_input: A ChatInput object containing the prompt and other parameters.

        Returns:
            A ChatOutput object containing the LLM's response.
        """
        pass
