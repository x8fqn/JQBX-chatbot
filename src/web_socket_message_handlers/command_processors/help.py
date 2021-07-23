from typing import Optional, Dict, List

from src.bot_controller import AbstractBotController, BotController
from src.web_socket_message_handlers.command_processors.abstract_command_processor import AbstractCommandProcessor
from src.web_socket_message_handlers.command_processors.command_processors import command_processors


class HelpCommandProcessor(AbstractCommandProcessor):
    def __init__(self, bot_controller: AbstractBotController = BotController.get_instance()):
        self.__commands: Dict[str, AbstractCommandProcessor] = {
            x.keyword: x for x in command_processors
        }
        self.__bot_controller = bot_controller

    @property
    def keyword(self) -> str:
        return 'help'

    @property
    def help(self) -> str:
        return 'This'

    def process(self, user_id: str, args: Optional[List[str]]) -> None: 
        if not args:
            self.__bot_controller.chat(
                ', '.join([self.__commands[key].keyword for key in sorted(self.__commands.keys())]))
        elif 'verbose' in args:
            self.__bot_controller.chat(
                ['/%s - %s' % (self.__commands[key].keyword, self.__commands[key].help) for key in sorted(self.__commands.keys())])
        elif (len(args) > 0) and (args[0] in [self.__commands[key].keyword for key in self.__commands.keys()]):
            self.__bot_controller.chat('/%s - %s' % (self.__commands[args[0]].keyword, self.__commands[args[0]].help))
            

