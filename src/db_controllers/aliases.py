from abc import ABC, abstractclassmethod, abstractmethod
import os, sqlite3
from datetime import datetime
from typing import Any, List
from src.helpers import get_config_path

class AbstractAliasesDB(ABC):
    @abstractmethod
    def add(self, command: str, name: str, user_id: str, processors: List[str]) -> bool:
        pass

    @abstractmethod
    def get_processor(self, alias: str) -> List[Any]:
        pass

    @abstractmethod
    def get_all(self) -> List[Any]: 
        pass

    @abstractmethod
    def count(self) -> int:
        pass

    @abstractmethod
    def remove(self, name: str) -> bool:
        pass

class AliasesDB():
    def __init__(self, name: str = 'commands') -> None:
        self.__connection = sqlite3.connect(os.path.join(get_config_path(), name + '.sqlite'))
        self.__init_table()

    def __init_table(self) -> None:
        query = '''
        CREATE TABLE IF NOT EXISTS aliases (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            processor TEXT,
            alias TEXT UNIQUE,
            user_id TEXT,
            timestamp FLOAT
        )
        '''
        self.__connection.cursor().execute(query)
        self.__connection.commit()

    def add(self, processor: str, name: str, user_id: str, processors: List[str]) -> bool:
        query = 'INSERT INTO aliases (processor, alias, user_id, timestamp) VALUES (?, ?, ?, ?)'
        if (name == processor) or (name in processors): return False
        try:
            self.__connection.cursor().execute(query, (processor, name, user_id, datetime.now().timestamp()))
            self.__connection.commit()
        except sqlite3.IntegrityError: return False
        else: return True

    def get_processor(self, alias: str) -> List[Any]:
        query = 'SELECT processor FROM aliases WHERE alias = ?'
        result = self.__connection.cursor().execute(query, (alias,)).fetchone()
        if result: return result[0] 
        else: return None 

    def get_all(self) -> List[Any]:
        query = 'SELECT alias FROM aliases'
        result = self.__connection.cursor().execute(query).fetchall()
        return [x[0] for x in result]

    def count(self) -> int:
        query = 'SELECT count(*) FROM aliases'
        result = self.__connection.cursor().execute(query).fetchone()
        return result[0]

    def remove(self, name: str) -> bool:
        query = 'DELETE FROM aliases WHERE alias = ?'
        result = self.__connection.cursor().execute(query, (name, ))
        self.__connection.commit()
        if result.rowcount > 0: return True
        if result.rowcount == 0: return False