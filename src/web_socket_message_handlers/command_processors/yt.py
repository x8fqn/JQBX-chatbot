from typing import Optional, List
from modules.youtube import Youtube
from bot_controller import AbstractBotController, BotController
from room_state import AbstractRoomState, RoomState
from web_socket_message_handlers.command_processors.abstract_command_processor import AbstractCommandProcessor


class YtCommandProcessor(AbstractCommandProcessor):
    def __init__(self, room_state: AbstractRoomState = RoomState.get_instance(),
                 bot_controller: AbstractBotController = BotController.get_instance()):
        self.__room_state = room_state
        self.__bot_controller = bot_controller

    @property
    def keyword(self) -> str:
        return 'yt'

    @property
    def help(self) -> str:
        return '''
            Listen to this tune on YouTube 
        '''

    def process(self, user_id: str, payload: Optional[str] = None) -> None:
        result = Youtube.searchTune(self.__room_state.current_track['name'], 
            [artist['name'] for artist in self.__room_state.current_track['artists']],
            self.__room_state.current_track['duration_ms'] // 1000)
        if result != False:
            self.__bot_controller.chat(result['url'])
        else:
            self.__bot_controller.chat('Couldn\'t find this on YouTube')
