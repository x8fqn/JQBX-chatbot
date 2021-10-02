import logging
from src.core import Core
from src.web_socket_message import WebSocketMessage
from src.web_socket_message_handlers.abstract_web_socket_message_handler import AbstractWebSocketMessageHandler
from src.web_socket_message_handlers.command_processors.first import FirstCommandProcessor, AbstractCommandProcessor

class PlayTrackHandler(AbstractWebSocketMessageHandler):
    def __init__(self, first_processor: AbstractCommandProcessor = FirstCommandProcessor()):
        self.__first_processor = first_processor

    @property
    def message_label(self) -> str:
        return 'play-track'

    def handle(self, message: WebSocketMessage, core: Core) -> None:
        core.room_state.set_current_track(message.payload)
        logging.debug('Track playing now: %s - %s' % (
                core.room_state.current_track['name'],
                ", ".join([i['name'] for i in core.room_state.current_track['artists']])
                ))
        if core.settings.autofirst_isEnabled:
            self.__first_processor.process(core.room_state.djs[0]['id'], None)
        core.spotify.playlist_add_items(core.settings.spotify_playlist_playback, [core.room_state.current_track['uri']])
