from typing import Optional, List, cast

from src.bot_controller import AbstractBotController, BotController
from src.web_socket_message_handlers.command_processors.abstract_command_processor import AbstractCommandProcessor
from udpy import UrbanClient, UrbanDefinition
from src.web_socket_message_handlers.objects.user_input import UserInput
from src.web_socket_message_handlers.objects.push_message import PushMessage


class UrbanCommandProcessor(AbstractCommandProcessor):
    def __init__(self, bot_controller: AbstractBotController = BotController.get_instance()):
        self.__bot_controller = bot_controller

    @property
    def keyword(self) -> str:
        return 'urban'

    @property
    def help(self) -> str:
        return 'Get the urban dictionary definition of a word'

    def process(self, pushMessage: PushMessage, userInput: UserInput) -> None:
        if not userInput.arguments:
            return self.__bot_controller.chat('Please provide a search query')
        args = userInput.text
        client = UrbanClient()
        dfns: List[UrbanDefinition] = cast(List[UrbanDefinition], client.get_definition(args))
        if not dfns:
            self.__bot_controller.chat('No definition found for "%s"' % args)
            return
        dfn = dfns[0]
        self.__bot_controller.chat([
            '%s: %s' % (dfn.word, dfn.definition),
            '',
            'Example:',
            dfn.example
        ])
