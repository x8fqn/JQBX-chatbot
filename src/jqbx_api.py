import requests
from abc import ABC, abstractmethod


class AbstractJQBXAPI(ABC):
    @abstractmethod
    def firsts(self, spotify_uri: str) -> dict:
        pass

    @abstractmethod
    def user(self, user_id: str) -> dict:
        pass

    @abstractmethod
    def room(self, room_id: str) -> dict:
        pass

    @abstractmethod
    def roomsActive(self, page = 0) -> dict:
        pass

    @abstractmethod
    def roomsAll(self, page: int) -> dict:
        pass
        
    @abstractmethod
    def promotions(self) -> dict:
        pass


class JQBXAPI(AbstractJQBXAPI):
    def firsts(self, spotify_uri: str) -> dict:
        # spotify:track:TRACK_ID
        return requests.get('https://jqbx.fm/tracks/first/%s' % spotify_uri).json()

    def user(self, user_id: str) -> dict:
        # spotify:user:USER_ID
        return requests.get('https://jqbx.fm/user/%s' % user_id).json()

    def room(self, room_id: str) -> dict:
        return requests.get('https://jqbx.fm/room/%s' % room_id).json()

    def roomsActive(self, page = 0) -> dict:
        return requests.get('https://jqbx.fm/active-rooms/%s' % str(page)).json()

    def roomsAll(self, page: int = 0) -> dict:
        return requests.get('https://jqbx.fm/active-rooms/%s' % str(page)).json()
    
    def promotions(self) -> dict:
        return requests.get('https://jqbx.fm/promotions').json()

