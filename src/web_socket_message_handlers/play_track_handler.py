from room_state import AbstractRoomState, RoomState
from web_socket_message import WebSocketMessage
from web_socket_message_handlers.abstract_web_socket_message_handler import AbstractWebSocketMessageHandler
from logger import AbstractLogger, Logger
from configuration import AbstractConfiguration, Configuration
from web_socket_message_handlers.command_processors.first import FirstProcessor
class PlayTrackHandler(AbstractWebSocketMessageHandler):
    def __init__(self, room_state: AbstractRoomState = RoomState.get_instance()):
        self.__room_state = room_state
        self.__logger: AbstractLogger = Logger()
        self.__config: AbstractConfiguration = Configuration('bot_main', '../config')

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
