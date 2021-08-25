from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Union
import os, sqlite3
from datetime import datetime
from src.helpers import get_config_path


class Command:
    def __init__(self, name: str, type: int, added_timestamp: float, command_id: int = None, publisher_id: str = None, description: str = None,
    updated_timestamp: float = None, updater_id: str = None) -> None:
        self.__name = name
        self.__type = type
        self.__publisher_id = publisher_id
        self.__description = description
        self.__command_id = command_id
        self.__added_timestamp = added_timestamp
        self.__updated_timestamp = updated_timestamp
        self.__updater_id = updater_id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def description(self) -> Optional[str]:
        return self.__description
    
    @property
    def type(self) -> int:
        return self.__type

    @property
    def publisher_id(self) -> str:
        return self.__publisher_id

    @property
    def command_id(self) -> int:
        return self.__command_id

    @property
    def updated_timestamp(self) -> float:
        return self.__updated_timestamp
    
    @property
    def updater_id(self) -> str:
        return self.__updater_id

    @property
    def added_timestamp(self) -> float:
        return self.__added_timestamp


class Alias(Command):
    def __init__(self, command: Command, keyword: str, alias_id: int) -> None:
        super().__init__(command.name, command.type, command.added_timestamp, command.command_id, command.publisher_id, command.description,
    command.updated_timestamp, command.updater_id)
        self.__keyword = keyword
        self.__alias_id = alias_id
    
    @property
    def alias_id(self) -> int:
        return self.__alias_id

    @property
    def keyword(self) -> str:
        return self.__keyword

class Single(Command):
    def __init__(self, command: Command, message: str, single_id: int) -> None:
        super().__init__(command.name, command.type, command.added_timestamp, command.command_id, command.publisher_id, command.description,
    command.updated_timestamp, command.updater_id)
        self.__single_id = single_id
        self.__message = message

    @property
    def single_id(self):
        return self.__single_id

    @property
    def message(self):
        return self.__message



class AbstractCustomCommandsDB(ABC):
    @abstractmethod
    def create_single(self, name: str, message: str, publisher_id: str = None, description: str = None) -> bool:
        pass

    @abstractmethod
    def create_alias(self, name: str, alias: str, publisher_id: str = None, description: str = None) -> bool:
        pass

    @abstractmethod
    def get_all_command_names(self) -> Optional[List[str]]:
        pass

    @abstractmethod
    def get_command(self, name: str) -> Optional[Union[Alias, Single]]:
        pass

    @abstractmethod
    def remove_command(self, command: Union[Single, Alias]) -> bool:
        pass

class CustomCommandsDB(AbstractCustomCommandsDB):
    def __init__(self, name: str = 'commands') -> None:
        self.__connection = sqlite3.connect(os.path.join(get_config_path(), name + '.sqlite'))
        self.__tables_init()

    @property
    def __types(self) -> List[str]:
        return ['SINGLE',
                'COLLECTION',
                'ALIAS',
                'ACTION']

    def __tables_init(self): 
        cur = self.__connection.cursor()
        cur.execute('PRAGMA foreign_keys=ON')
        query = ''' 
        CREATE TABLE IF NOT EXISTS commands (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            name TEXT UNIQUE NOT NULL,
            type INTEGER NOT NULL,
            description TEXT,
            publisher_id TEXT,
            last_updated REAL,
            updater_id TEXT,
            added_timestamp REAL NOT NULL
        )'''
        cur.execute(query)
        query = '''
        CREATE TABLE IF NOT EXISTS aliases (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
            keyword TEXT NOT NULL,
            command_id INTEGER UNIQUE NOT NULL,
            FOREIGN KEY (command_id) REFERENCES commands(id) ON DELETE CASCADE
        )
        '''
        cur.execute(query)
        query = '''
        CREATE TABLE IF NOT EXISTS singles (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
            message TEXT NOT NULL,
            command_id INTEGER UNIQUE NOT NULL,
            FOREIGN KEY (command_id) REFERENCES commands(id) ON DELETE CASCADE
        )
        '''
        cur.execute(query)
        query = '''
        CREATE TABLE IF NOT EXISTS collections (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
            message TEXT NOT NULL,
            publisher_id TEXT,
            timestamp REAL NOT NULL,
            command_id INTEGER NOT NULL,
            FOREIGN KEY (command_id) REFERENCES commands(id) ON DELETE CASCADE
        )
        '''
        cur.execute(query)
        self.__connection.commit()

    def __create_command(self, name: str, type: int, publisher_id: str = None, description: str = None) -> sqlite3.Cursor:
        query = 'INSERT INTO commands (name, type, description, publisher_id, added_timestamp) VALUES (?, ?, ?, ?, ?)'
        cur = self.__connection.cursor()
        timestamp = datetime.now().timestamp()
        cur.execute(query, (name, type, description, publisher_id, timestamp))
        return cur

    def create_single(self, name: str, message: str, publisher_id: str = None, description: str = None) -> bool:
        query = 'INSERT INTO singles (message, command_id) VALUES (?, ?)'
        type = 0
        cur = self.__create_command(name, type, publisher_id, description)
        command_id = cur.lastrowid
        cur.execute(query, (message, command_id))
        self.__connection.commit()
        return True
    
    def create_alias(self, name: str, alias: str, publisher_id: str = None, description: str = None) -> bool:
        query = 'INSERT INTO aliases (keyword, command_id) VALUES (?, ?)'
        type = 2
        cur = self.__create_command(name, type, publisher_id, description)
        command_id = cur.lastrowid
        cur.execute(query, (alias, command_id))
        self.__connection.commit()
        return True

    # def create_collection(self, name: str, type: int = 1, publisher: str = None, description: str = None) -> bool:
    #     cur = self.__connection.cursor()
    #     query = 'INSERT INTO commands (name, type, description, publisher_id, timestamp) VALUES (?, ?, ?, ?, ?)'
    #     cur.execute(query, (name, type, publisher, description, datetime.now().timestamp()))

    def get_all_command_names(self) -> Optional[List[str]]:
        cur = self.__connection.cursor()
        query = 'SELECT name FROM commands'
        result = cur.execute(query).fetchall()
        names = []
        for command in result:
            names.append(command[0])
        return names

    def get_command(self, name: str) -> Optional[Union[Alias, Single]]:
        cur = self.__connection.cursor()
        query = 'SELECT name, type, added_timestamp, id, publisher_id, description FROM commands WHERE name = ?'
        result = cur.execute(query, (name, )).fetchone()
        # Returns None if not found and break
        if not result: return None
        command = Command(result[0], result[1], result[2], result[3], result[4], result[5])
        # Type: single
        if command.type == 0:
            return self.__get_single(command)
        # Type: alias
        elif command.type == 2: 
            return self.__get_alias(command)

    def remove_command(self, command: Union[Single, Alias]) -> bool:
        query = 'DELETE FROM commands WHERE id = ?'
        cur = self.__connection.cursor()
        cur.execute(query, (command.command_id,))
        self.__connection.commit()
        return True

    def __get_alias(self, command: Command) -> Optional[Alias]:
        cur = self.__connection.cursor()
        # query = 'SELECT aliases.id, aliases.keyword FROM aliases JOIN commands ON aliases.command_id = commands.id WHERE commands.id = ?'
        query = 'SELECT keyword, id FROM aliases WHERE command_id = ?'
        result = cur.execute(query, (command.command_id,)).fetchone()
        return Alias(command, keyword=result[0], alias_id=result[1])
        
    def __get_single(self, command: Command) -> Optional[Single]:
        cur = self.__connection.cursor()
        query = 'SELECT message, id FROM singles WHERE command_id = ?'
        result = cur.execute(query, (command.command_id,)).fetchone()
        return Single(command, message=result[0], single_id=result[1])

