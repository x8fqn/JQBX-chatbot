from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Union
from src.bot_controller import AbstractBotController, BotController
from src.db_controllers.custom_commands import Single, Alias, CustomCommandsDB, AbstractCustomCommandsDB

from src.web_socket_message_handlers.objects.user_input import UserInput
from src.web_socket_message_handlers.objects.push_message import PushMessage

class AbstractCommandController(ABC):
    @abstractmethod
    def create_single(self, name: str, message: str, publisher_id: str = None, description: str = None) -> bool:
        pass

    @abstractmethod
    def create_alias(self, name: str, alias: str, publisher_id: str = None, description: str = None) -> bool:
        pass

    @abstractmethod
    def get_command(self, name: str) -> Optional[Union[Alias, Single]]:
        pass

    @abstractmethod
    def remove_command(self, command: Union[Single, Alias]) -> bool:
        pass

    @abstractmethod
    def command_list(self) -> Optional[List[str]]:
        pass


class CommandController(AbstractCommandController):
    __instance: Optional['CommandController'] = None

    def __init__(self, custom_commands: AbstractCustomCommandsDB = CustomCommandsDB(),
    bot_controller: AbstractBotController = BotController.get_instance()) -> None:
        self.__commands = custom_commands
        self.__bot_controller = bot_controller
        CommandController.__instance = self
    
    def get_instance() -> 'CommandController':
        if CommandController.__instance is None:
            CommandController()
        return CommandController.__instance

    def command_list(self) -> Optional[List[str]]:
        return self.__commands.get_all_command_names()

    def create_single(self, name: str, message: str, publisher_id: str = None, description: str = None) -> bool:
        return self.__commands.create_single(name, message, publisher_id, description)

    def create_alias(self, name: str, alias: str, publisher_id: str = None, description: str = None) -> bool:
        return self.__commands.create_alias(name, alias, publisher_id, description)

    def get_command(self, name: str) -> Optional[Union[Alias, Single]]:
        return self.__commands.get_command(name)

    def remove_command(self, command: Union[Single, Alias]) -> bool:
        return self.__commands.remove_command(command)

  