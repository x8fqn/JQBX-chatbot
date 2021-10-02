from src.core import Core
from src.web_socket_message import WebSocketMessage
from src.web_socket_message_handlers.abstract_web_socket_message_handler import AbstractWebSocketMessageHandler


class KeepAwakeHandler(AbstractWebSocketMessageHandler):
    def __init__(self):
        pass

    @property
    def message_label(self) -> str:
        return 'keepAwake'

    def handle(self, message: WebSocketMessage, core: Core) -> None:
        core.ws_client.send(WebSocketMessage(label='stayAwake', payload={'date': message.payload['date']}))
        core.ws_client.send(WebSocketMessage(2))
