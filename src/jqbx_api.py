from typing import List, Optional
import requests
from abc import ABC, abstractmethod

class External_urls:
    def __init__(self, ext_urls: dict) -> None:
        self.__ext_urls = ext_urls

    @property
    def spotify(self) -> str:
        return self.__ext_urls.get('spotify')

class Profile():
    def __init__(self, user_request: dict) -> None:
        self.__request = user_request
        
    @property
    def uri(self) -> str:
        return self.__request.get('uri')
    
    @property
    def country(self) -> str:
        return self.__request.get('country')
    
    @property
    def display_name(self) -> str:
        return self.__request.get('display_name')
    
    @property
    def device(self) -> str:
        return self.__request.get('device')

    @property    
    def external_urls(self) -> Optional[External_urls]:
        ext_urls = self.__request.get('external_urls')
        if ext_urls:
            return External_urls(ext_urls)
        return ext_urls 
    
    @property
    def href(self) -> str:
        return self.__request.get('href')
    
    @property
    def id(self) -> str:
        return self.__request.get('id')
    
    @property
    def firstTime(self) -> Optional[bool]:
        return self.__request.get('firstTime')
    
    @property
    def username(self) -> Optional[str]:
        return self.__request.get('username')
    
    @property
    def canFollow(self) -> Optional[bool]:
        return self.__request.get('canFollow')
    
    @property
    def image(self) -> Optional[str]:
        return self.__request.get('image')
    
    @property
    def thumbsUpImage(self) -> Optional[str]:
        return self.__request.get('thumbsUpImage')
    
    @property
    def thumbsDownImage(self) -> Optional[str]:
        return self.__request.get('thumbsDownImage')
    
    @property
    def djImage(self) -> Optional[str]:
        return self.__request.get('djImage')
    
    @property
    def status(self) -> Optional[str]:
        return self.__request.get('status')
    
    @property
    def thumbsUp(self) -> Optional[int]:
        return self.__request.get('thumbsUp')
    
    @property
    def stars(self) -> Optional[int]:
        return self.__request.get('stars')
    
    @property
    def thumbsDown(self) -> Optional[int]:
        return self.__request.get('thumbsDown')
    
    @property
    def following(self) -> Optional[List]:
        return self.__request.get('following')
    
    @property
    def canNotify(self) -> Optional[bool]:
        return self.__request.get('canNotify')
    
    @property
    def keepAfterPlay(self) -> Optional[bool]:
        return self.__request.get('keepAfterPlay')
    
    @property
    def pushToTop(self) -> Optional[bool]:
        return self.__request.get('pushToTop')
    
    @property
    def pushPlaylistsToTop(self) -> Optional[bool]:
        return self.__request.get('pushPlaylistsToTop')
    
    @property
    def hideStatsUri(self) -> Optional[bool]:
        return self.__request.get('hideStatsUri')
    
    @property
    def showPushNotifications(self) -> Optional[bool]:
        return self.__request.get('showPushNotifications')
    
    @property
    def soundcloud(self) -> Optional[str]:
        return self.__request.get('soundcloud')
    
    @property
    def instagram(self) -> Optional[str]:
        return self.__request.get('instagram')
    
    @property
    def twitter(self) -> Optional[str]:
        return self.__request.get('twitter')
    
    @property
    def lastDjNotification(self) -> int:
        return self.__request.get('lastDjNotification')
    
    @property
    def lastfm(self) -> Optional[str]:
        return self.__request.get('lastfm')
    
    @property
    def website(self) -> Optional[str]:
        return self.__request.get('website')
    
    @property
    def showImagesInChat(self) -> Optional[bool]:
        return self.__request.get('showImagesInChat')
    
    @property
    def userWhitelist(self) -> Optional[List]:
        return self.__request.get('userWhitelist')
    
    @property
    def acceptsMarketing(self) -> Optional[bool]:
        return self.__request.get('acceptsMarketing')
    
    @property
    def openLinksWithSpotify(self) -> Optional[bool]:
        return self.__request.get('openLinksWithSpotify')
    
    @property
    def disableConfetti(self) -> Optional[bool]:
        return self.__request.get('disableConfetti')
    
    @property
    def distractionFreeMode(self) -> Optional[bool]:
        return self.__request.get('distractionFreeMode')
    
    @property
    def hideUserImages(self) -> Optional[bool]:
        return self.__request.get('hideUserImages')
    
    @property
    def hideTrackImages(self) -> Optional[bool]:
        return self.__request.get('hideTrackImages')
    
    @property
    def hideSpotifyUri(self) -> Optional[bool]:
        return self.__request.get('hideSpotifyUri')
    
    @property
    def alwaysInactive(self) -> Optional[bool]:
        return self.__request.get('alwaysInactive')
    
    @property
    def inRoom(self) -> Optional[str]:
        return self.__request.get('inRoom')
    
    @property
    def roomId(self) -> Optional[str]:
        return self.__request.get('roomId')
    
    @property
    def roomTitle(self) -> Optional[str]:
        return self.__request.get('roomTitle')
    
    @property
    def roomHandle(self) -> Optional[str]:
        return self.__request.get('roomHandle')

    def primaryUsername(self) -> str:
        return self.username if self.username else self.display_name

class AbstractJQBXAPI(ABC):
    @abstractmethod
    def firsts(cls, spotify_uri: str) -> dict:
        pass

    @abstractmethod
    def user(cls, user_id: str) -> Profile:
        pass

    @abstractmethod
    def room(cls, room_id: str) -> dict:
        pass

    @abstractmethod
    def roomsActive(cls, page = 0) -> dict:
        pass

    @abstractmethod
    def roomsAll(cls, page: int) -> dict:
        pass

    @abstractmethod
    def roomsSearch(cls, title: str, page: int = 0) -> dict:
        pass

    @abstractmethod
    def promotions(cls) -> dict:
        pass

    
class JQBXAPI(AbstractJQBXAPI):
    @classmethod
    def firsts(cls, spotify_uri: str) -> dict:
        # spotify:track:TRACK_ID
        return requests.get('https://jqbx.fm/tracks/first/%s' % spotify_uri).json()

    @classmethod
    def user(cls, user_id: str) -> Profile:
        # spotify:user:USER_ID
        req = requests.get('https://jqbx.fm/user/%s' % user_id).json()
        return Profile(req)
    
    @classmethod
    def room(cls, room_id: str) -> dict:
        return requests.get('https://jqbx.fm/room/%s' % room_id).json()

    @classmethod
    def roomsActive(cls, page = 0) -> dict:
        return requests.get('https://jqbx.fm/active-rooms/%s' % str(page)).json()

    @classmethod
    def roomsAll(cls, page: int = 0) -> dict:
        return requests.get('https://jqbx.fm/active-rooms/%s' % str(page)).json()

    @classmethod
    def roomsSearch(cls, title: str, page: int = 0) -> dict:
        return requests.get('https://jqbx.fm/rooms/search/title/%s/' % str(page)).json()
    
    @classmethod
    def promotions(cls) -> dict:
        return requests.get('https://jqbx.fm/promotions').json()

