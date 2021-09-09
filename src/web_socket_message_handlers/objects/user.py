from typing import Dict, Optional

__all__ = ['User']

class User:
    def __init__(self, user: Dict[str, Dict]) -> None:
        self.__user_obj = user

    @property
    def username(self) -> str:
        return self.__user_obj.get('username', None)

    @property
    def display_name(self) -> str:
        return self.__user_obj.get('display_name')

    @property
    def id(self) -> str:
        return self.__user_obj.get('id', None)

    @property
    def uri(self) -> str:
        return self.__user_obj.get('uri', None)

    @property
    def device(self) -> str:
        return self.__user_obj.get('device', None)

    @property
    def status(self) -> str:
        return self.__user_obj.get('status', None)

    @property
    def country(self) -> str:
        return self.__user_obj.get('country', None)

    @property
    def image(self) -> Optional[str]:
        return self.__user_obj.get('image', None)

    @property
    def thumbsUpImage(self) -> Optional[str]:
        return self.__user_obj.get('thumbsUpImage', None)

    @property
    def thumbsDownImage(self) -> Optional[str]:
        return self.__user_obj.get('thumbsUpImage', None)

    @property
    def djImage(self) -> Optional[str]:
        return self.__user_obj.get('djImage', None)

    @property
    def statusChangedAt(self) -> Optional[str]:
        return self.__user_obj.get('statusChangedAt', None)

    @property
    def _id(self) -> Optional[str]:
        return self.__user_obj.get('_id', None)