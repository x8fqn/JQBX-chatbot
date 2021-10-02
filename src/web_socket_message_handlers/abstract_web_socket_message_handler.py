from abc import ABC, abstractmethod
from src.core import Core
from src.web_socket_message import WebSocketMessage
from src.web_socket_client import AbstractWebSocketClient


class AbstractWebSocketMessageHandler(ABC):
    @property
    @abstractmethod
    def message_label(self) -> str:
        pass

    @abstractmethod
    def handle(self, message: WebSocketMessage, core: Core) -> None:
        pass
