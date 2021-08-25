from src.web_socket_message_handlers.objects.user_input import UserInput
from src.web_socket_message_handlers.objects.push_message import PushMessage
from src.bot_controller import AbstractBotController, BotController
from src.web_socket_message_handlers.command_processors.abstract_command_processor import AbstractCommandProcessor
from src.command_controller import AbstractCommandController, CommandController


class SingleProcessor(AbstractCommandProcessor):
    def __init__(self, bot_controller: AbstractBotController = BotController.get_instance(),
    command_controller: AbstractCommandController = CommandController.get_instance()) -> None:
        self.__bot_controller = bot_controller
        self.__command_controller = command_controller

    @property
    def keyword(self) -> str:
        return 'single'

    @property
    def help(self) -> str:
        return 'Creates cingle line messages'

    def process(self, pushMessage: PushMessage, userInput: UserInput) -> None:
        help_msg = 'Possible options: /single {name} {message} {description (optional)}'
        if userInput.arguments:
            name, message = userInput.args_get(0), userInput.args_get(1)
            description = userInput.args_get(2)
            if message and name:
                if self.__command_controller.create_single(name, message, pushMessage.user.id, description):
                    self.__bot_controller.chat('Done!')
                else:
                    self.__bot_controller.chat('Failed!')
            else:
                self.__bot_controller.chat(help_msg)
        else:
            self.__bot_controller.chat(help_msg)

