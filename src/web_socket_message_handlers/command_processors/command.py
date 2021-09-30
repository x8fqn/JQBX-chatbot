from src.web_socket_message_handlers.objects.user_input import UserInput
from src.web_socket_message_handlers.objects.push_message import PushMessage
from src.web_socket_message_handlers.command_processors.abstract_command_processor import AbstractCommandProcessor
from src.command_controller import AbstractCommandController
from src.bot_controller import AbstractBotController
from src.command_controller import AbstractCommandController
from src.room_state import AbstractRoomState
from src.settings import AbstractSettings


class CommandCommandProcessor(AbstractCommandProcessor):
    @property
    def keyword(self) -> str:
        return 'command'

    @property
    def help(self) -> str:
        return 'Commands control'

    def process(self, pushMessage: PushMessage, userInput: UserInput,
    bot_controller: AbstractBotController, room_state: AbstractRoomState, settings: AbstractSettings, command_controller: AbstractCommandController) -> None:
        help_msg = 'Using: /command remove {command_name}'
        if userInput.arguments:
            cmd_name = userInput.args_get(1)
            if cmd_name:
                if userInput.args_check('remove', 0):
                    command = command_controller.get_command(cmd_name)
                    if command_controller.remove_command(command):
                        bot_controller.info_chat('Done!')
                    else:
                        bot_controller.info_chat('Failed!')
            else:
                bot_controller.chat(help_msg)
        else:
            bot_controller.chat(help_msg)

