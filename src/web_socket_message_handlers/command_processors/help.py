from typing import Optional, Dict, List
from src.command_controller import AbstractCommandController, CommandController

from src.bot_controller import AbstractBotController, BotController
from src.web_socket_message_handlers.command_processors.abstract_command_processor import AbstractCommandProcessor
from src.web_socket_message_handlers.command_processors.command_processors import Processors
from src.web_socket_message_handlers.objects.user_input import UserInput
from src.web_socket_message_handlers.objects.push_message import PushMessage


class HelpCommandProcessor(AbstractCommandProcessor):
    def __init__(self, bot_controller: AbstractBotController = BotController.get_instance(),
    command_controller: AbstractCommandController = CommandController.get_instance(),
    processors = Processors()):
        self.__processors = processors
        self.__bot_controller = bot_controller
        self.__command_controller = command_controller

    @property
    def keyword(self) -> str:
        return 'help'

    @property
    def help(self) -> str:
        return 'This'

    def process(self, pushMessage: PushMessage, userInput: UserInput) -> None: 
        msg = [
        '%s: %s' % ('Built-ins', ', '.join(self.__processors.command_processors.keys())),
        '%s: %s' % ('Custom commands', ', '.join(self.__command_controller.command_list()))]
        if not pushMessage.recipients:
            self.__bot_controller.chat(msg)
        else:
            self.__bot_controller.whisper(msg, pushMessage.payload.get('user'))
