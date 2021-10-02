from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Union
from src.db_controllers.custom_commands import Single, Alias, CustomCommandsDB, AbstractCustomCommandsDB

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
    def __init__(self, custom_commands: AbstractCustomCommandsDB = CustomCommandsDB()) -> None:
        self.__commands = custom_commands

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

  