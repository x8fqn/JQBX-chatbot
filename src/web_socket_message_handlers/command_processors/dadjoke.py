from typing import Optional, List
from dadjokes import dadjokes

from src.web_socket_message_handlers.command_processors.abstract_command_processor import AbstractCommandProcessor
from src.web_socket_message_handlers.objects.user_input import UserInput
from src.web_socket_message_handlers.objects.push_message import PushMessage
from src.command_controller import AbstractCommandController
from src.bot_controller import AbstractBotController
from src.command_controller import AbstractCommandController
from src.room_state import AbstractRoomState
from src.settings import AbstractSettings


class DadjokeCommandProcessor(AbstractCommandProcessor):

    @property
    def keyword(self) -> str:
        return 'dadjoke'

    @property
    def help(self) -> str:
        return 'Hi, I\'m Dad.'

    def process(self, pushMessage: PushMessage, userInput: UserInput,
    bot_controller: AbstractBotController, room_state: AbstractRoomState, settings: AbstractSettings, command_controller: AbstractCommandController) -> None:
        bot_controller.chat(dadjokes.Dadjoke().joke)
