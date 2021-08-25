from typing import Optional, List

from src.bot_controller import AbstractBotController, BotController
from src.data_service import DataService, AbstractDataService
from src.web_socket_message_handlers.command_processors.abstract_command_processor import AbstractCommandProcessor
from src.room_state import AbstractRoomState, RoomState
from src.web_socket_message_handlers.objects.user_input import UserInput
from src.web_socket_message_handlers.objects.push_message import PushMessage


class ThemeCommandProcessor(AbstractCommandProcessor):
    def __init__(self, bot_controller: AbstractBotController = BotController.get_instance(),
                 room_state: AbstractRoomState = RoomState.get_instance(),
                 data_service: AbstractDataService = DataService()):
        self.__bot_controller = bot_controller
        self.__room_state = room_state
        self.__data_service = data_service

    @property
    def keyword(self) -> str:
        return 'theme'

    @property
    def help(self) -> str:
        return '''
            See the current theme
        '''

    def process(self, pushMessage: PushMessage, userInput: UserInput) -> None:
        current_welcome_message = self.__data_service.get_welcome_message()
        if current_welcome_message:
            self.__bot_controller.chat(current_welcome_message)
        else:
            self.__bot_controller.chat('The theme is not currently set.')
