from src.web_socket_message_handlers.objects.user_input import UserInput
from src.web_socket_message_handlers.objects.push_message import PushMessage
from src.web_socket_message_handlers.command_processors.abstract_command_processor import AbstractCommandProcessor
from src.command_controller import AbstractCommandController
from src.bot_controller import AbstractBotController
from src.command_controller import AbstractCommandController
from src.room_state import AbstractRoomState
from src.settings import AbstractSettings


class AliasesProcessor(AbstractCommandProcessor):
    @property
    def keyword(self) -> str:
        return 'alias'

    @property
    def help(self) -> str:
        return 'Alias management'

    def process(self, pushMessage: PushMessage, userInput: UserInput,
    bot_controller: AbstractBotController, room_state: AbstractRoomState, settings: AbstractSettings, command_controller: AbstractCommandController) -> None:
        help_msg = 'Possible options: /alias {new alias name} {command to alias} {description (optional)}'
        if userInput.arguments:
            name, keyword = userInput.args_get(0), userInput.args_get(1)
            description = userInput.args_get(2)
            if keyword and name:
                if command_controller.create_alias(name, keyword, pushMessage.user.id, description):
                    bot_controller.info_chat('Done! Alias of %s command is created. Use /%s to try it out' % (keyword, name))
                else:
                    bot_controller.info_chat('Failed to create /%s alias of /%s! Possibly, this name is already in use' % (name, keyword))
            else:
                bot_controller.chat(help_msg)
        else:
            bot_controller.chat(help_msg)
