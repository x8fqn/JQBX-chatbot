from src.settings import AbstractSettings
from src.web_socket_client import AbstractWebSocketClient, WebSocketClient
from src.web_socket_message import WebSocketMessage
from src.bot_controller import AbstractBotController
from src.command_controller import AbstractCommandController
from src.room_state import AbstractRoomState
from src.settings import AbstractSettings
from src.web_socket_message_handlers.abstract_web_socket_message_handler import AbstractWebSocketMessageHandler


class KeepAwakeHandler(AbstractWebSocketMessageHandler):
    def __init__(self):
        pass

    @property
    def message_label(self) -> str:
        return 'keepAwake'

    def handle(self, message: WebSocketMessage, web_socket_client: AbstractWebSocketClient,
    settings: AbstractSettings, bot_controller: AbstractBotController,
    room_state: AbstractRoomState, command_controller: AbstractCommandController) -> None:
        web_socket_client.send(WebSocketMessage(label='stayAwake', payload={'date': message.payload['date']}))
        web_socket_client.send(WebSocketMessage(2))
