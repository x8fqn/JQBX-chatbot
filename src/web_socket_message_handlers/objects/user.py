from typing import Dict, Optional

__all__ = ['User']

class User:
    def __init__(self, user: Dict[str, Dict]) -> None:
        self.__username = user.get('username', None)
        self.__display_name = user.get('display_name')
        self.__id = user.get('id', None)
        self.__uri = user.get('uri', None)
        self.__device = user.get('device', None) # bot, mobile, desktop
        self.__status = user.get('status', None) # active, inactive
        self.__country = user.get('country', None) # UK, US, BY ...
        self.__image = user.get('image', None)
        self.__thumbsUpImage = user.get('thumbsUpImage', None)
        self.__thumbsDownImage = user.get('thumbsDownImage', None)
        self.__djImage = user.get('djImage', None)
        self.__statusChangedAt = user.get('statusChangedAt', None)
        self.___id = user.get('_id', None)

    @property
    def username(self) -> str:
        return self.__username

    @property
    def display_name(self) -> str:
        return self.__display_name

    @property
    def id(self) -> str:
        return self.__id

    @property
    def uri(self) -> str:
        return self.__uri

    @property
    def device(self) -> str:
        return self.__device

    @property
    def status(self) -> str:
        return self.__status

    @property
    def country(self) -> str:
        return self.__country

    @property
    def image(self) -> Optional[str]:
        return self.__image

    @property
    def thumbsUpImage(self) -> Optional[str]:
        return self.__thumbsUpImage

    @property
    def thumbsDownImage(self) -> Optional[str]:
        return self.__thumbsDownImage

    @property
    def djImage(self) -> Optional[str]:
        return self.__djImage

    @property
    def statusChangedAt(self) -> Optional[str]:
        return self.__statusChangedAt

    @property
    def _id(self) -> Optional[str]:
        return self.___id