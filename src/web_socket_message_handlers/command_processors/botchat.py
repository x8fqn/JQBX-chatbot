from src.web_socket_message_handlers.objects.user_input import UserInput
from src.web_socket_message_handlers.objects.push_message import PushMessage
from src.bot_controller import AbstractBotController, BotController
from src.web_socket_message_handlers.command_processors.abstract_command_processor import AbstractCommandProcessor
from src.command_controller import AbstractCommandController, CommandController


class SpeakCommandProcessor(AbstractCommandProcessor):
    def __init__(self, bot_controller: AbstractBotController = BotController.get_instance(),
    command_controller: AbstractCommandController = CommandController.get_instance()) -> None:
        self.__bot_controller = bot_controller
        self.__command_controller = command_controller

    @property
    def keyword(self) -> str:
        return 'speak'

    @property
    def help(self) -> str:
        return ''

    def process(self, pushMessage: PushMessage, userInput: UserInput) -> None:
        self.__bot_controller.chat(userInput.text)


class AlertCommandProcessor(AbstractCommandProcessor):
    def __init__(self, bot_controller: AbstractBotController = BotController.get_instance(),
    command_controller: AbstractCommandController = CommandController.get_instance()) -> None:
        self.__bot_controller = bot_controller
        self.__command_controller = command_controller

    @property
    def keyword(self) -> str:
        return 'alert'

    @property
    def help(self) -> str:
        return ''

    def process(self, pushMessage: PushMessage, userInput: UserInput) -> None:
        self.__bot_controller.info_chat(userInput.text)
        

