from src.room_state import AbstractRoomState, RoomState
from src.web_socket_message import WebSocketMessage
from src.web_socket_message_handlers.abstract_web_socket_message_handler import AbstractWebSocketMessageHandler
from src.logger import AbstractLogger, Logger
from src.configuration import AbstractConfiguration, Configuration
from src.web_socket_message_handlers.command_processors.first import FirstProcessor
class PlayTrackHandler(AbstractWebSocketMessageHandler):
    def __init__(self, room_state: AbstractRoomState = RoomState.get_instance(),
                logger: AbstractLogger = Logger(),
                config: AbstractConfiguration = Configuration('bot_main', 'config')):
        self.__room_state = room_state
        self.__logger = logger
        self.__config = config

    @property
    def message_label(self) -> str:
        return 'play-track'

    def handle(self, message: WebSocketMessage) -> None:
        self.__room_state.set_current_track(message.payload)
        self.__logger.info('Track playing now: %s - %s' % (
                self.__room_state.current_track['name'],
                ", ".join([i['name'] for i in self.__room_state.current_track['artists']])
                ))
        if self.__config.update()['auto-first'] == True:
            FirstProcessor().process(self.__room_state.djs[0]['id'], None)
            pass
