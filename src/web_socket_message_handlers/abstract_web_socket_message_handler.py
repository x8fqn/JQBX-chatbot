from abc import ABC, abstractmethod
from src.bot_controller import AbstractBotController
from src.command_controller import AbstractCommandController
from src.room_state import AbstractRoomState
from src.settings import AbstractSettings

from src.web_socket_message import WebSocketMessage
from src.web_socket_client import AbstractWebSocketClient


class AbstractWebSocketMessageHandler(ABC):
    @property
    @abstractmethod
    def message_label(self) -> str:
        pass

    @abstractmethod
    def handle(self, message: WebSocketMessage, web_socket_client: AbstractWebSocketClient,
    settings: AbstractSettings, bot_controller: AbstractBotController,
    room_state: AbstractRoomState, command_controller: AbstractCommandController) -> None:
        pass
