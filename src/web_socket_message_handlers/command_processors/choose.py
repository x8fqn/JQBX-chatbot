import random
from typing import Optional, List

from src.web_socket_message_handlers.command_processors.abstract_command_processor import AbstractCommandProcessor
from src.web_socket_message_handlers.objects.user_input import UserInput
from src.web_socket_message_handlers.objects.push_message import PushMessage
from src.command_controller import AbstractCommandController
from src.bot_controller import AbstractBotController
from src.command_controller import AbstractCommandController
from src.room_state import AbstractRoomState
from src.settings import AbstractSettings


class ChooseCommandProcessor(AbstractCommandProcessor):
    @property
    def keyword(self) -> str:
        return 'choose'

    @property
    def help(self) -> str:
        return 'Pick something randomly from a comma-separated list of choices'

    def process(self, pushMessage: PushMessage, userInput: UserInput,
    bot_controller: AbstractBotController, room_state: AbstractRoomState, settings: AbstractSettings, command_controller: AbstractCommandController) -> None:
        if not userInput.arguments:
            return bot_controller.chat('Please give me a comma-separate list of choices')
        bot_controller.chat(random.choice(userInput.text.split(',')).strip())
