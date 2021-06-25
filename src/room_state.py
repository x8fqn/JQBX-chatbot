import os
from helpers import get_main_dir
from abc import ABC, abstractmethod
from typing import List, Optional

from bot_controller import BotController, AbstractBotController
from logger import Logger, AbstractLogger
from track_history import TrackLogger
from dateutil import parser


class AbstractRoomState(ABC):
    @property
    @abstractmethod
    def room_title(self) -> Optional[str]:
        pass

    @property
    @abstractmethod
    def mod_ids(self) -> List[str]:
        pass

    @property
    @abstractmethod
    def users(self) -> List[dict]:
        pass

    @property
    @abstractmethod
    def djs(self) -> List[dict]:
        pass

    @property
    @abstractmethod
    def current_track(self) -> Optional[dict]:
        pass

    @property
    def votes(self) -> Optional[dict]:
        pass
    
    @abstractmethod
    def set_room_title(self, room_title: str) -> None:
        pass

    @abstractmethod
    def set_mod_ids(self, mod_ids: List[str]) -> None:
        pass

    @abstractmethod
    def set_users(self, users: List[dict]) -> None:
        pass

    @abstractmethod
    def set_djs(self, djs: List[dict]) -> None:
        pass

    @abstractmethod
    def set_current_track(self, current_track: dict) -> None:
        pass

    @abstractmethod
    def set_votes(self, thumbsUp: int, thumbsDown: int, stars: int) -> None:
        pass


class RoomState(AbstractRoomState):
    __instance: Optional['RoomState'] = None

    def __init__(self, bot_controller: AbstractBotController, logger: AbstractLogger = Logger()):
        if RoomState.__instance:
            raise Exception('Use get_instance() instead!')
        self.__mod_ids: List[str] = []
        self.__users: List[dict] = []
        self.__djs: List[dict] = []
        self.__current_track: Optional[dict] = None
        self.__thumbUp_count: int = None
        self.__thumbDown_count: int = None
        self.__star_count: int = None
        self.__bot_controller = bot_controller
        self.__room_title: Optional[str] = None
        self.__logger = logger
        self.__track_logger = TrackLogger()
        self.__track_logger.connect(os.path.join(get_main_dir(), '..', 'config', 'track_history.sqlite'))
        RoomState.__instance = self

    @staticmethod
    def get_instance(bot_controller: AbstractBotController = BotController.get_instance()) -> 'RoomState':
        if RoomState.__instance is None:
            RoomState(bot_controller)
        return RoomState.__instance

    @property
    def room_title(self) -> Optional[str]:
        return self.__room_title

    @property
    def mod_ids(self) -> List[str]:
        return self.__mod_ids

    @property
    def users(self) -> List[dict]:
        return self.__users

    @property
    def djs(self) -> List[dict]:
        return self.__djs

    @property
    def current_track(self) -> Optional[dict]:
        return self.__current_track

    @property
    def votes(self) -> Optional[dict]:
        return {
            'thumbUp': self.__thumbUp_count,
            'thumbDown': self.__thumbDown_count,
            'star': self.__star_count
        }

    def set_mod_ids(self, mod_ids: List[str]) -> None:
        self.__mod_ids = mod_ids

    def set_users(self, users: List[dict]) -> None:
        self.__users = users

    def set_djs(self, djs: List[dict]) -> None:
        self.__djs = djs

    def set_current_track(self, current_track: dict) -> None:
        self.__current_track = current_track
        self.__track_logger.add_track(self.__current_track['name'],
            ", ".join([i['name'] for i in self.__current_track['artists']]),
            self.__current_track['uri'], parser.parse(self.__current_track['startedAt']).timestamp(),
            self.__current_track['userUri'])
        self.__bot_controller.reset_vote()

    def set_room_title(self, room_title: str) -> None:
        if self.__room_title != room_title:
            self.__room_title = room_title
            self.__logger.info('Room title changed: %s' % room_title)

    def set_votes(self, thumbUp_count: int, thumbDown_count: int, star_count: int) -> None:
        self.__thumbUp_count = thumbUp_count
        self.__thumbDown_count = thumbDown_count
        self.__star_count = star_count
        self.__track_logger.update_track_votes(parser.parse(self.__current_track['startedAt']).timestamp(), 
            self.__thumbUp_count, self.__thumbDown_count, self.__star_count)