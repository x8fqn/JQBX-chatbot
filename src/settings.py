from abc import ABC, abstractmethod
# from src.bot_controller import AbstractBotController, BotController
from src.config import AbstractConfig, Config
from src.helpers import get_bot_user 


class AbstractSettings(ABC):
    @property
    @abstractmethod
    def log_level(self) -> int:
        pass

    @property
    @abstractmethod
    def user(self) -> dict:
        pass

    @property
    @abstractmethod
    def user_id(self) -> str:
        pass

    @property
    @abstractmethod
    def room_id(self) -> str:
        pass

    @abstractmethod
    def set_username(self, username: str):
        pass

    @abstractmethod
    def set_image(self, type: int, image_link: str):
        pass
    
    @abstractmethod
    def welcome_set_message(self, message: str) -> None:
        pass

    @property
    @abstractmethod
    def welcome_message(self) -> str:
        pass

    @abstractmethod
    def welcome_set_enable(self, enable: bool) -> None:
        pass

    @property
    @abstractmethod
    def welcome_isEnabled(self) -> bool:
        pass

    @abstractmethod
    def welcome_set_whisper(self, enable: bool) -> None:
        pass

    @property
    @abstractmethod
    def welcome_isWhisper(self) -> bool:
        pass
    
    @abstractmethod
    def autofirst_set_enable(self, enable: bool) -> None:
        pass

    @property
    @abstractmethod
    def autofirst_isEnabled(self) -> bool:
        pass

    @property
    @abstractmethod
    def spotify_refresh_token(self) -> str:
        pass

    @property
    @abstractmethod
    def spotify_client_id(self) -> str:
        pass

    @property
    @abstractmethod
    def spotify_client_secret(self) -> str:
        pass

    @property
    @abstractmethod
    def spotify_playlist_playback(self) -> str:
        pass

    
class Settings(AbstractSettings):
    def __init__(self, config: AbstractConfig = Config()):
        self.__config = config
        self.__bot_user = get_bot_user(self.__config.get('username'), self.__config.get('user_id'), self.__config.get('image_url'), 
            self.__config.get('thumbsUpImage_url'), self.__config.get('thumbsDownImage_url'), self.__config.get('djImage_url'))

    @property
    def log_level(self) -> int:
        return self.__config.get('log_level')
    
    @property
    def user(self) -> dict:
        return self.__bot_user

    @property
    def user_id(self) -> str:
        return self.__bot_user['id']

    @property
    def room_id(self) -> str:
        return self.__config.get('room_id')

    def set_username(self, username: str):
        self.__bot_user.update({'username': username})
        self.__config.set('username', username)
    
    def set_image(self, type: int, image_link: str):
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

    def welcome_set_message(self, message: str) -> None:
        self.__config.set('welcome_message', message.strip())

    @property
    def welcome_message(self) -> str:
        message = self.__config.get('welcome_message')
        return 'No message' if message == (None or '') else message

    def welcome_set_enable(self, enable: bool) -> None:
        self.__config.set('welcome_enabled', enable)
    
    @property
    def welcome_isEnabled(self) -> bool:
        status = self.__config.get('welcome_enabled')
        return False if status == None else status

    def welcome_set_whisper(self, enable: bool) -> None:
        self.__config.set('welcome_whisper', enable)
    
    @property
    def welcome_isWhisper(self) -> bool:
        status = self.__config.get('welcome_whisper')
        return status if status else None

    def autofirst_set_enable(self, enable: bool) -> None:
        self.__config.set('auto-first_enabled', enable)

    @property
    def autofirst_isEnabled(self) -> bool:
        status = self.__config.get('auto-first_enabled')
        return status if status else None

    @property
    def spotify_refresh_token(self) -> str:
        token = self.__config.get('spotify_refresh_token')
        return token if token else None

    @property
    def spotify_client_id(self) -> str:
        client_id = self.__config.get('spotify_client_id')
        return client_id if client_id else None

    @property
    def spotify_client_secret(self) -> str:
        client_secret = self.__config.get('spotify_client_secret')
        return client_secret if client_secret else None

    @property
    def spotify_playlist_playback(self) -> str:
        playlist_playback = self.__config.get('spotify_playlist_playback')
        return playlist_playback if playlist_playback else None