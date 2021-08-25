from typing import Optional, List

from src.bot_controller import AbstractBotController, BotController
from src.web_socket_message_handlers.command_processors.abstract_command_processor import AbstractCommandProcessor
from dadjokes import dadjokes
from src.web_socket_message_handlers.objects.user_input import UserInput
from src.web_socket_message_handlers.objects.push_message import PushMessage

class DadjokeCommandProcessor(AbstractCommandProcessor):
    def __init__(self, bot_controller: AbstractBotController = BotController.get_instance()):
        self.__bot_controller = bot_controller

    @property
    def keyword(self) -> str:
        return 'dadjoke'

    @property
    def help(self) -> str:
        return 'Hi, I\'m Dad.'

    def process(self, pushMessage: PushMessage, userInput: UserInput) -> None:
        self.__bot_controller.chat(dadjokes.Dadjoke().joke)
