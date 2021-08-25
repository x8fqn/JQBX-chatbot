import random
from typing import Optional, List

from src.bot_controller import AbstractBotController, BotController
from src.web_socket_message_handlers.command_processors.abstract_command_processor import AbstractCommandProcessor
from src.web_socket_message_handlers.objects.user_input import UserInput
from src.web_socket_message_handlers.objects.push_message import PushMessage


class ChooseCommandProcessor(AbstractCommandProcessor):
    def __init__(self, bot_controller: AbstractBotController = BotController.get_instance()):
        self.__bot_controller = bot_controller

    @property
    def keyword(self) -> str:
        return 'choose'

    @property
    def help(self) -> str:
        return 'Pick something randomly from a list of choices'

    def process(self, pushMessage: PushMessage, userInput: UserInput) -> None:
        if not userInput.arguments:
            return self.__bot_controller.chat('Please give me a comma-separate list of choices')
        self.__bot_controller.chat(random.choice(userInput.arguments).strip())
