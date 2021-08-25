import logging, os
from src.helpers import get_main_dir
from abc import ABC, abstractmethod
from typing import List, Optional

from src.bot_controller import BotController, AbstractBotController
from src.db_controllers.track_history import AbstractTrackHistory, TrackHistory
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
    @abstractmethod
    def votes(self) -> Optional[dict]:
        pass

    @property
    @abstractmethod
    def max_user_count(self) -> int:
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
    def set_votes(self, thumbsUp: int, thumbsDown: int, stars: int, max_user_count: int) -> None:
        pass


class RoomState(AbstractRoomState):
    __instance: Optional['RoomState'] = None

    def __init__(self, bot_controller: AbstractBotController, track_history: AbstractTrackHistory = TrackHistory()):
        if RoomState.__instance:
            raise Exception('Use get_instance() instead!')
        self.__mod_ids: List[str] = []
        self.__users: List[dict] = []
        self.__djs: List[dict] = []
        self.__current_track: Optional[dict] = None
        self.__thumbUp_count: int = None
        self.__thumbDown_count: int = None
        self.__star_count: int = None
        self.__max_user_count: int = None
        self.__bot_controller = bot_controller
        self.__room_title: Optional[str] = None
        self.__track_history = track_history
        RoomState.__instance = self

    @staticmethod
    def get_instance(bot_controller: AbstractBotController = BotController.get_instance(),
    track_history: AbstractTrackHistory = TrackHistory()) -> 'RoomState':
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
            'thumbsUp': self.__thumbUp_count,
            'thumbsDown': self.__thumbDown_count,
            'stars': self.__star_count
        }
    
    @property
    def max_user_count(self) -> int:
        return self.__max_user_count

    def set_mod_ids(self, mod_ids: List[str]) -> None:
        self.__mod_ids = mod_ids

    def set_users(self, users: List[dict]) -> None:
        self.__users = users
        new_user_count = len(users)
        current_user_count = len(self.users)
        if new_user_count > current_user_count:
            self.__max_user_count = new_user_count

    def set_djs(self, djs: List[dict]) -> None:
        self.__djs = djs

    def set_current_track(self, current_track: dict) -> None:
        self.__current_track = current_track
        self.__max_user_count = len(self.users)
        self.__track_history.add_track(self.__current_track['name'],
            ", ".join([i['name'] for i in self.__current_track['artists']]),
            self.__current_track['uri'], parser.parse(self.__current_track['startedAt']).timestamp(),
            self.__current_track['userUri'], self.__max_user_count)
        self.__bot_controller.reset_vote()

    def set_room_title(self, room_title: str) -> None:
        if self.__room_title != room_title:
            self.__room_title = room_title
            logging.info('Room title changed: %s' % room_title , )

    def set_votes(self, thumbUp_count: int, thumbDown_count: int, star_count: int, max_user_count: int) -> None:
        self.__thumbUp_count = thumbUp_count
        self.__thumbDown_count = thumbDown_count
        self.__star_count = star_count
        self.__track_history.update_track_votes(parser.parse(self.__current_track['startedAt']).timestamp(), 
            thumbUp_count, thumbDown_count, star_count, max_user_count)