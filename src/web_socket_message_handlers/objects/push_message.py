from typing import Dict, List, Optional
from src.web_socket_message import WebSocketMessage
from .user import User

__all__ = ['PushMessage']

class PushMessage:
    def __init__(self, payload: WebSocketMessage) -> None:
        '''Object of `push-message` payload
        Fields: message, user, recipients, selectingEmoji, type, _id
        '''
        self.__payload = payload.payload
        self.__message = self.__payload.get('message', None)
        self.__selectingEmoji = self.__payload.get('selectingEmoji', None)
        self.__user = User(self.__payload.get('user')) if self.__payload.get('user') else None
        self.__recipients = [User(user) for user in self.__payload.get('recipients')] if self.__payload.get('recipients') else None
        self.__type = self.__payload.get('type', None)
        self.___id = self.__payload.get('_id', None)
    
    @property
    def user(self) -> Optional[User]:
        '''`User` object or `None`'''
        return self.__user

    @property
    def recipients(self) -> Optional[List[User]]:
        '''List of `User` objects or `None`'''
        return self.__recipients

    @property
    def message(self) -> str:
        return self.__message

    @property
    def type(self) -> Optional[str]:
        return self.__type
    
    @property
    def selectingEmoji(self) -> Optional[bool]:
        return self.__selectingEmoji
    
    @property
    def _id(self) -> Optional[str]:
        return self.___id

