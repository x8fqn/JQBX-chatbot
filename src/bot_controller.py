import os
from abc import ABC, abstractmethod
from typing import List, Optional, Union

from src.configuration import AbstractConfiguration, Configuration
from src.helpers import get_bot_user, get_config_path
from src.web_socket_client import AbstractWebSocketClient, WebSocketClient
from src.web_socket_message import WebSocketMessage


class AbstractBotController(ABC):
    @abstractmethod
    def chat(self, message: Union[str, List[str]]) -> None:
        pass
    
    @abstractmethod
    def interroom_chat(self, room_id: str, username: str, message: str) -> None:
        pass
    
    @abstractmethod
    def whisper(self, message: str, recipient: dict) -> None:
        pass

    @abstractmethod
    def dope(self) -> None:
        pass

    @abstractmethod
    def nope(self) -> None:
        pass

    @property
    @abstractmethod
    def star(self) -> None:
        pass

    @property
    @abstractmethod
    def doped(self) -> bool:
        pass

    @property
    @abstractmethod
    def noped(self) -> bool:
        pass

    @property
    @abstractmethod
    def starred(self) -> bool:
        pass
    
    @abstractmethod
    def reset_vote(self) -> None:
        pass


class BotController(AbstractBotController):
    __instance: Optional['BotController'] = None

    def __init__(self, config: AbstractConfiguration = Configuration('bot_main'),
                 web_socket_client: AbstractWebSocketClient = WebSocketClient.get_instance()):
        if BotController.__instance:
            raise Exception('Use get_instance() instead!')
        self.__config = config
        self.__bot_user = get_bot_user(self.__config.get('username'), self.__config.get('user_id'), self.__config.get('image_url'), 
            self.__config.get('thumbsUpImage_url'), self.__config.get('thumbsDownImage_url'), self.__config.get('djImage_url'))
        self.__web_socket_client = web_socket_client
        self.__doped: bool = False
        self.__noped: bool = False
        BotController.__instance = self

    @staticmethod
    def get_instance() -> 'BotController':
        if BotController.__instance is None:
            BotController()
        return BotController.__instance

    def chat(self, message: Union[str, List[str]]) -> None:
        lines = message if isinstance(message, list) else [message]
        payload = {
            'roomId': self.__config.get()['jqbx_room_id'],
            'user': self.__bot_user,
            'message': {
                'message': ' <br/> '.join(lines),
                'user': self.__bot_user,
                'selectingEmoji': False
            }
        }
        self.__web_socket_client.send(WebSocketMessage(label='chat', payload=payload))

    def interroom_chat(self, room_id: str, username: str, message: str) -> None:
        payload = {
            'roomId': room_id,
            'user': self.__bot_user,
            'message': {
                'message': message,
                'user': self.__bot_user,
                'selectingEmoji': False
            }
        }
        payload['message']['user']['username'] = username
        self.__web_socket_client.send(WebSocketMessage(label='chat', payload=payload))

    def whisper(self, message: str, recipient: dict) -> None:
        bot_user = self.__bot_user
        payload = {
            'roomId': self.__config.get()['jqbx_room_id'],
            'user': bot_user,
            'message': {
                'message': '%s' % message,
                'user': bot_user,
                'recipients': [
                    recipient,
                    bot_user
                ],
                'selectingEmoji': False
            }
        }
        self.__web_socket_client.send(WebSocketMessage(label='chat', payload=payload))

    def updateUsername(self, username: str) -> None:
        self.__bot_user.update({'username': username})
        payload = self.__bot_user
        self.__web_socket_client.send(WebSocketMessage(label='updateUserInfo', payload=payload))

    def updateImage(self, image_link: str, type: int) -> None:
        if type == 0:
            typeName = 'image'
        elif type == 1:
            typeName = 'thumbsUpImage'
        elif type == 2:
            typeName = 'thumbsDownImage'
        elif type == 3:
            typeName = 'djImage'
        self.__bot_user.update({typeName: image_link})
        self.__config.set(typeName + '_url', image_link)
        payload = self.__bot_user
        self.__web_socket_client.send(WebSocketMessage(label='updateUserInfo', payload=payload))

    def dope(self) -> None:
        if self.__doped or self.__noped:
            return
        self.__web_socket_client.send(WebSocketMessage(label='thumbsUp', payload={
            'roomId': self.__config.get()['jqbx_room_id'],
            'user': self.__bot_user
        }))
        self.__doped = True

    def nope(self) -> None:
        if self.__doped or self.__noped:
            return
        self.__web_socket_client.send(WebSocketMessage(label='thumbsDown', payload={
            'roomId': self.__config.get()['jqbx_room_id'],
            'user': self.__bot_user
        }))
        self.__noped = True

    def star(self) -> None:
        if self.__starred:
            return
        self.__web_socket_client.send(WebSocketMessage(label='starTrack', payload={
            'roomId': self.__config.get()['jqbx_room_id'],
            'user': self.__bot_user
        }))
        self.__starred = True

    @property
    def doped(self) -> bool:
        return self.__doped

    @property
    def noped(self) -> bool:
        return self.__noped

    @property
    def starred(self) -> bool:
        return self.__starred

    def reset_vote(self) -> None:
        self.__doped = False
        self.__noped = False
        self.__starred = False
