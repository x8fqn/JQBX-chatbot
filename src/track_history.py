import sqlite3
from typing import Optional

class TrackLogger():
    __instance: Optional['TrackLogger'] = None

    def __init__(self) -> None:
        TrackLogger.__instance = self

    def get_instance() -> 'TrackLogger':
        if TrackLogger.__instance is None:
            TrackLogger()
        return TrackLogger.__instance

    def connect(self, path) -> bool:
        self.__connection = None
        try:
            self.__connection = sqlite3.connect(path)
            self.__initialize_table(self.__connection)
            return True
        except sqlite3.Error as e:
            raise RuntimeError('database connection error') from e

    def __initialize_table(self, connection: sqlite3.Connection):
        query = """
        CREATE TABLE IF NOT EXISTS track_history (
            name TEXT,
            artist TEXT,
            track_uri TEXT,
            timestamp REAL NOT NULL,
            user_id TEXT,
            thumbsUp INTEGER DEFAULT 0,
            thumbsDown INTEGER DEFAULT 0,
            stars INTEGER DEFAULT 0
        )"""
        try:
            connection.execute(query)
        except sqlite3.Error as e: 
            raise RuntimeError('initializing table error') from e

    def add_track(self, name: str, artist: str, track_uri: str, timestamp: float, user_id: str) -> bool:
        query = "INSERT INTO track_history (name, artist, track_uri, timestamp, user_id) VALUES (?, ?, ?, ?, ?)"
        try:
            self.__connection.cursor().execute(query, (name, artist, track_uri, timestamp, user_id))
            self.__connection.commit()
        except sqlite3.Error as e: 
            raise RuntimeError('add_track error') from e

    def update_track_votes(self, timestamp: float, thumbUp_count: int, thumbDown_count: int, star_count: int) -> bool:
        query = "UPDATE track_history SET thumbsUp = ?, thumbsDown = ?, stars = ? WHERE timestamp = ?"
        try:
            self.__connection.cursor().execute(query, (thumbUp_count, thumbDown_count, star_count, timestamp))
            self.__connection.commit()
        except sqlite3.Error as e: 
            raise RuntimeError('update_track_votes error') from e

 
            