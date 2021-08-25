from typing import Optional, List
from src.modules.youtube import Youtube
from src.bot_controller import AbstractBotController, BotController
from src.room_state import AbstractRoomState, RoomState
from src.web_socket_message_handlers.command_processors.abstract_command_processor import AbstractCommandProcessor
from src.web_socket_message_handlers.objects.user_input import UserInput
from src.web_socket_message_handlers.objects.push_message import PushMessage


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
            Find the link to this tune on YouTube
        '''

    def process(self, pushMessage: PushMessage, userInput: UserInput) -> None:
        result = Youtube.searchTune(self.__room_state.current_track['name'], 
            [artist['name'] for artist in self.__room_state.current_track['artists']],
            self.__room_state.current_track['duration_ms'] // 1000)
        if result != False:
            self.__bot_controller.chat('%s#.jpg %s' % (result['thumbnail'], result['url']))
        else:
            self.__bot_controller.chat('Couldn\'t find this on YouTube')
