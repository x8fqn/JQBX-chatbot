from abc import ABC, abstractmethod
from typing import Dict, List, Optional

from src.db_controllers.aliases import AbstractAliasesDB, AliasesDB

class AbstractCommandController(ABC):
    @abstractmethod
    def alias_get_all(self) -> Optional[List]:
        pass

    @abstractmethod
    def alias_add(self, alias: str, processor: str, user_id: str, processors: List[str]) -> bool:
        pass

    @abstractmethod
    def alias_get_processor(self, keyword: str) -> Optional[str]:
        pass

    @abstractmethod
    def alias_remove(self, alias: str) -> bool:
        pass

    @property
    @abstractmethod
    def command_keywords(self) -> List[str]:
        pass

    @abstractmethod
    def set_keywords(self, keywords: List[str]) -> None:
        pass 


class CommandController(AbstractCommandController):
    __instance: Optional['CommandController'] = None

    def __init__(self, alias: AbstractAliasesDB = AliasesDB()) -> None:
        self.__command_keywords: Optional[List[str]] = None
        self.__alias = alias

        CommandController.__instance = self
    
    def get_instance() -> 'CommandController':
        if CommandController.__instance is None:
            CommandController()
        return CommandController.__instance

    def set_keywords(self, keywords: List[str]) -> None:
        self.__command_keywords = keywords

    @property
    def command_keywords(self) -> List[str]:
        return self.__command_keywords

    def alias_add(self, alias: str, processor: str, user_id: str, commands: List[str]) -> bool:
        return self.__alias.add(processor, alias, user_id, commands)

    def alias_get_processor(self, keyword: str) -> Optional[str]:
        return self.__alias.get_processor(keyword)
    
    def alias_get_all(self) -> Optional[List]:
        return self.__alias.get_all()

    def alias_remove(self, alias: str) -> bool:
        return self.__alias.remove(alias)