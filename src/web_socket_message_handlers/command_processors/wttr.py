from typing import Optional, List
from src.bot_controller import AbstractBotController, BotController
from src.room_state import AbstractRoomState, RoomState
from src.web_socket_message_handlers.command_processors.abstract_command_processor import AbstractCommandProcessor
from src.web_socket_message_handlers.objects.user_input import UserInput
from src.web_socket_message_handlers.objects.push_message import PushMessage
from urllib.parse import quote


class WttrCommandProcessor(AbstractCommandProcessor):
    def __init__(self, bot_controller: AbstractBotController = BotController.get_instance()):
        self.__bot_controller = bot_controller

    @property
    def keyword(self) -> str:
        return 'wttr'

    @property
    def help(self) -> str:
        return '''
            Display the weather
        '''

    def process(self, pushMessage: PushMessage, userInput: UserInput) -> None:
        url = 'http://wttr.in/%s_q0np.png' % (quote(userInput.text if userInput.text else ''))
        self.__bot_controller.chat(url)


