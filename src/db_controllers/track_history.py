from abc import ABC, abstractmethod
import sqlite3, os
from typing import Optional
from src.helpers import get_config_path

class AbstractTrackHistory(ABC):
    @abstractmethod
    def add_track(self, name: str, artist: str, track_uri: str, timestamp: float, user_id: str, max_user_count: int = 0) -> bool:
        pass

    @abstractmethod
    def update_track_votes(self, timestamp: float, thumbUp_count: int, thumbDown_count: int, star_count: int, max_user_count: int) -> bool:
        pass


class TrackHistory(AbstractTrackHistory):
    def __init__(self, name: str = 'trackHistory'):
        self.__connection = sqlite3.connect(os.path.join(get_config_path(), name + '.sqlite'))
        self.__initialize_table(self.__connection)

    def __initialize_table(self, connection: sqlite3.Connection):
        query = """
        CREATE TABLE IF NOT EXISTS track_history (
            name TEXT,
            artist TEXT,
            track_uri TEXT,
            timestamp REAL NOT NULL,
            user_id TEXT,
            max_user_count INTEGER DEFAULT 0,
            thumbsUp INTEGER DEFAULT 1,
            thumbsDown INTEGER DEFAULT 0,
            stars INTEGER DEFAULT 0
        )"""
        connection.execute(query)

    def add_track(self, name: str, artist: str, track_uri: str, timestamp: float, user_id: str, max_user_count: int) -> bool:
        if timestamp < 1000: return False
        query = "INSERT INTO track_history (name, artist, track_uri, timestamp, user_id, max_user_count) VALUES (?, ?, ?, ?, ?, ?)"
        self.__connection.cursor().execute(query, (name, artist, track_uri, timestamp, user_id, max_user_count))
        self.__connection.commit()

    def update_track_votes(self, timestamp: float, thumbUp_count: int, thumbDown_count: int, star_count: int, max_user_count: int = 0) -> bool:
        query = "UPDATE track_history SET thumbsUp = ?, thumbsDown = ?, stars = ?, max_user_count = ? WHERE timestamp = ?"
        self.__connection.cursor().execute(query, (thumbUp_count, thumbDown_count, star_count, max_user_count, timestamp))
        self.__connection.commit()
            