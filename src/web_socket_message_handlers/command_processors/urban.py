from typing import List, cast

from src.web_socket_message_handlers.command_processors.abstract_command_processor import AbstractCommandProcessor
from udpy import UrbanClient, UrbanDefinition
from src.web_socket_message_handlers.objects.user_input import UserInput
from src.web_socket_message_handlers.objects.push_message import PushMessage
from src.command_controller import AbstractCommandController
from src.bot_controller import AbstractBotController
from src.command_controller import AbstractCommandController
from src.room_state import AbstractRoomState
from src.settings import AbstractSettings


class UrbanCommandProcessor(AbstractCommandProcessor):
    @property
    def keyword(self) -> str:
        return 'urban'

    @property
    def help(self) -> str:
        return 'Get the urban dictionary definition of a word'

    def process(self, pushMessage: PushMessage, userInput: UserInput,
    bot_controller: AbstractBotController, room_state: AbstractRoomState, settings: AbstractSettings, command_controller: AbstractCommandController) -> None:
        if not userInput.arguments:
            return bot_controller.chat('Please provide a search query')
        args = userInput.text
        client = UrbanClient()
        dfns: List[UrbanDefinition] = cast(List[UrbanDefinition], client.get_definition(args))
        if not dfns:
            bot_controller.chat('No definition found for "%s"' % args)
            return
        dfn = dfns[0]
        bot_controller.chat([
            '%s: %s' % (dfn.word, dfn.definition),
            '',
            'Example:',
            dfn.example
        ])
