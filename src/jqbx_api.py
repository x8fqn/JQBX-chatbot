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
        request = requests.get('https://jqbx.fm/tracks/first/%s' % spotify_uri).json()
        return request

    def user(user_id: str) -> dict:
        # spotify:user:USER_ID
        request = requests.get('https://jqbx.fm/user/%s' % user_id).json()
        return request

    def room(room_id: str) -> dict:
        request = requests.get('https://jqbx.fm/room/%s' % room_id).json()
        return request

    def roomsActive(page: int = 0) -> dict:
        request = requests.get('https://jqbx.fm/active-rooms/%s' % str(page)).json()
        return request

    def roomsAll(page: int = 0) -> dict:
        request = requests.get('https://jqbx.fm/active-rooms/%s' % str(page)).json()
        return request
        
    def promotions() -> dict:
        request = requests.get('https://jqbx.fm/promotions').json()
        return request

