from src.web_socket_message_handlers.command_processors.abstract_command_processor import AbstractCommandProcessor
from src.web_socket_message_handlers.command_processors.command_processors import Processors
from src.web_socket_message_handlers.objects.user_input import UserInput
from src.web_socket_message_handlers.objects.push_message import PushMessage
from src.command_controller import AbstractCommandController
from src.bot_controller import AbstractBotController
from src.command_controller import AbstractCommandController
from src.room_state import AbstractRoomState
from src.settings import AbstractSettings


class HelpCommandProcessor(AbstractCommandProcessor):
    def __init__(self, processors = Processors()):
        self.__processors = processors

    @property
    def keyword(self) -> str:
        return 'help'

    @property
    def help(self) -> str:
        return 'This'

    def process(self, pushMessage: PushMessage, userInput: UserInput,
    bot_controller: AbstractBotController, room_state: AbstractRoomState, settings: AbstractSettings, command_controller: AbstractCommandController) -> None: 
        msg = [
        '%s: %s' % ('Built-ins', ', '.join(self.__processors.command_processors.keys())),
        '%s: %s' % ('Custom commands', ', '.join(command_controller.command_list()))]
        if not pushMessage.recipients:
            bot_controller.chat(msg)
        else:
            bot_controller.whisper(msg, pushMessage.payload.get('user'))
