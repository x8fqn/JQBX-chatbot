from src.web_socket_message_handlers.objects.user_input import UserInput
from src.web_socket_message_handlers.objects.push_message import PushMessage
from src.bot_controller import AbstractBotController, BotController
from src.web_socket_message_handlers.command_processors.abstract_command_processor import AbstractCommandProcessor
from src.command_controller import AbstractCommandController, CommandController


class CommandCommandProcessor(AbstractCommandProcessor):
    def __init__(self, bot_controller: AbstractBotController = BotController.get_instance(),
    command_controller: AbstractCommandController = CommandController.get_instance()) -> None:
        self.__bot_controller = bot_controller
        self.__command_controller = command_controller

    @property
    def keyword(self) -> str:
        return 'command'

    @property
    def help(self) -> str:
        return 'Commands control'

    def process(self, pushMessage: PushMessage, userInput: UserInput) -> None:
        help_msg = 'Possible options: /command remove {command_name}'
        if userInput.arguments:
            cmd_name = userInput.args_get(1)
            if cmd_name:
                if userInput.args_check('remove', 0):
                    command = self.__command_controller.get_command(cmd_name)
                    if self.__command_controller.remove_command(command):
                        self.__bot_controller.info_chat('Done!')
                    else:
                        self.__bot_controller.info_chat('Failed!')
            else:
                self.__bot_controller.chat(help_msg)
        else:
            self.__bot_controller.chat(help_msg)

