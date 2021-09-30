from src.web_socket_message_handlers.objects.user_input import UserInput
from src.web_socket_message_handlers.objects.push_message import PushMessage
from src.web_socket_message_handlers.command_processors.abstract_command_processor import AbstractCommandProcessor
from src.command_controller import AbstractCommandController
from src.bot_controller import AbstractBotController
from src.command_controller import AbstractCommandController
from src.room_state import AbstractRoomState
from src.settings import AbstractSettings


class SingleProcessor(AbstractCommandProcessor):

    @property
    def keyword(self) -> str:
        return 'single'

    @property
    def help(self) -> str:
        return 'Creates single line messages'

    def process(self, pushMessage: PushMessage, userInput: UserInput,
    bot_controller: AbstractBotController, room_state: AbstractRoomState, settings: AbstractSettings, command_controller: AbstractCommandController) -> None:
        help_msg = 'Using: /single {command name} {message text} {description (optional)}'
        if userInput.arguments:
            name, message = userInput.args_get(0), userInput.args_get(1)
            description = userInput.args_get(2)
            if message and name:
                if command_controller.create_single(name, message, pushMessage.user.id, description):
                    bot_controller.info_chat('Done! Static command /%s is created' % name)
                else:
                    bot_controller.info_chat('Failed to create /%s command! Possibly, this name is already in use' % name)
            else:
                bot_controller.chat(help_msg)
        else:
            bot_controller.chat(help_msg)
