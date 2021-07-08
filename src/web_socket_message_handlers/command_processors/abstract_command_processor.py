from abc import ABC, abstractmethod
from typing import List, Optional


class AbstractCommandProcessor(ABC):
    @property
    @abstractmethod
    def keyword(self) -> str:
        pass

    @property
    @abstractmethod
    def help(self) -> str:
        pass

    @abstractmethod
    def process(self, user_id: str, args: Optional[List[str]]) -> None:
        pass
