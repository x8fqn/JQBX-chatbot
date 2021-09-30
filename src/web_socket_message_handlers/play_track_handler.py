import logging
from src.room_state import AbstractRoomState, RoomState
from src.web_socket_message import WebSocketMessage
from src.web_socket_message_handlers.abstract_web_socket_message_handler import AbstractWebSocketMessageHandler
from src.web_socket_client import AbstractWebSocketClient
from src.bot_controller import AbstractBotController
from src.command_controller import AbstractCommandController
from src.room_state import AbstractRoomState
from src.settings import AbstractSettings
from src.web_socket_message_handlers.command_processors.first import FirstCommandProcessor, AbstractCommandProcessor

class PlayTrackHandler(AbstractWebSocketMessageHandler):
    def __init__(self, first_processor: AbstractCommandProcessor = FirstCommandProcessor()):
        self.__first_processor = first_processor

    @property
    def message_label(self) -> str:
        return 'play-track'

    def handle(self, message: WebSocketMessage, web_socket_client: AbstractWebSocketClient,
    settings: AbstractSettings, bot_controller: AbstractBotController,
    room_state: AbstractRoomState, command_controller: AbstractCommandController) -> None:
        room_state.set_current_track(message.payload)
        logging.debug('Track playing now: %s - %s' % (
                room_state.current_track['name'],
                ", ".join([i['name'] for i in self.__room_state.current_track['artists']])
                ))
        if settings.autofirst_isEnabled:
            self.__first_processor.process(self.__room_state.djs[0]['id'], None)
