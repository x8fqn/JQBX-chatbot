from typing import Dict, List, Optional
from src.web_socket_message import WebSocketMessage
from .user import User

__all__ = ['PushMessage']

class PushMessage:
    def __init__(self, payload: WebSocketMessage) -> None:
        '''Object of `push-message` payload
        Fields: message, user, recipients, selectingEmoji, type, _id
        '''
        self.payload = payload.payload
        self.__message = self.payload.get('message', None)
        self.__selectingEmoji = self.payload.get('selectingEmoji', None)
        self.__user = User(self.payload.get('user')) if self.payload.get('user') else None
        self.__recipients = [User(user) for user in self.payload.get('recipients')] if self.payload.get('recipients') else None
        self.__type = self.payload.get('type', None)
        self.___id = self.payload.get('_id', None)
    
    @property
    def user(self) -> Optional[User]:
        '''`User` object or `None`'''
        return User(self.payload.get('user')) if self.payload.get('user') else None

    @property
    def recipients(self) -> Optional[List[User]]:
        '''List of `User` objects or `None`'''
        return [User(user) for user in self.payload.get('recipients')] if self.payload.get('recipients') else None

    @property
    def message(self) -> str:
        return self.payload.get('message', None)

    @property
    def type(self) -> Optional[str]:
        return self.payload.get('type', None)
    
    @property
    def selectingEmoji(self) -> Optional[bool]:
        return self.payload.get('selectingEmoji', None)
    
    @property
    def _id(self) -> Optional[str]:
        return self.payload.get('_id', None)

