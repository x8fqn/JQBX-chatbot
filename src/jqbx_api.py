import requests
from abc import ABC, abstractmethod
from requests.api import request


class AbstractJQBXAPI(ABC):
    @abstractmethod
    def firsts(spotify_uri: str) -> dict:
        pass

    @abstractmethod
    def user(user_id: str) -> dict:
        pass

    @abstractmethod
    def room(room_id: str) -> dict:
        pass

    @abstractmethod
    def roomsActive(page: int = 0) -> dict:
        pass

    @abstractmethod
    def roomsAll(page: int = 0) -> dict:
        pass
        
    @abstractmethod
    def promotions() -> dict:
        pass


class JQBXAPI(AbstractJQBXAPI):
    def firsts(spotify_uri: str) -> dict:
        # spotify:track:TRACK_ID
        return requests.get('https://jqbx.fm/tracks/first/%s' % spotify_uri).json()

    def user(user_id: str) -> dict:
        # spotify:user:USER_ID
        return requests.get('https://jqbx.fm/user/%s' % user_id).json()

    def room(room_id: str) -> dict:
        return requests.get('https://jqbx.fm/room/%s' % room_id).json()

    def roomsActive(page: int = 0) -> dict:
        return requests.get('https://jqbx.fm/active-rooms/%s' % str(page)).json()

    def roomsAll(page: int = 0) -> dict:
        return requests.get('https://jqbx.fm/active-rooms/%s' % str(page)).json()
    
    def promotions() -> dict:
        return requests.get('https://jqbx.fm/promotions').json()

