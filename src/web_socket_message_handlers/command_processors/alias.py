from typing import Dict, List, Optional
from src.bot_controller import AbstractBotController, BotController

from src.web_socket_message_handlers.command_processors.abstract_command_processor import AbstractCommandProcessor
from src.command_controller import AbstractCommandController, CommandController

class AliasesProcessor(AbstractCommandProcessor):
    def __init__(self, bot_controller: AbstractBotController = BotController.get_instance(),
    command_controller: AbstractCommandController = CommandController.get_instance()) -> None:
        self.__bot_controller = bot_controller
        self.__command_controller = command_controller

    @property
    def keyword(self) -> str:
        return 'alias'

    @property
    def help(self) -> str:
        return 'Alias management'

    def process(self, user_id: str, args: Optional[List[str]]) -> None:
        if args == []:
            self.__bot_controller.chat('Aliases: %s' % ' ,'.join(self.__command_controller.alias_get_all()))
        elif 'add' in args[0]:
            if self.__command_controller.alias_add(args[2], args[1], user_id, self.__command_controller.command_keywords):
                self.__bot_controller.chat('Alias added')
            else: 
                self.__bot_controller.chat('Command with this name already exists')
        elif 'remove' in args[0]:
            if self.__command_controller.alias_remove(args[1]):
                self.__bot_controller.chat('Alias removed')
            else: 
                self.__bot_controller.chat('Alias not removed')
        else: 
            self.__bot_controller.chat('Possible options: add {command} {alias} / remove {alias}')
