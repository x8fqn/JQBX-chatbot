import os, io, json 
from typing import List, Union
from abc import ABC, abstractmethod

class AbstractConfiguration(ABC):
    @abstractmethod
    def get(self) -> dict:
        pass

    @abstractmethod
    def add(self, key: str, data: Union[List, str]) -> bool:
        pass

    @abstractmethod
    def set(self, key: str, data: Union[List, str]) -> bool:
        pass

    @abstractmethod
    def remove(self, key: str, list_item: Union[int, str] = None) -> bool:
        pass

class Configuration(AbstractConfiguration):
    def __init__(self, name: str, path: str) -> None:
        self.__name = name
        self.__path = path
        self.__filename = self.__name + '.json'
        self.__config = dict
        if not self.__path.endswith(os.sep):
            self.__path += os.sep 
        if not os.path.exists(self.__path):
            os.mkdir(self.__path)
        if not os.path.isfile(self.__path + "/" + self.__filename):
            self.__init()
            
    def __init(self) -> None:
        with io.open(self.__path + self.__filename, 'w') as handle:
            handle.write(json.dumps({'module_name': self.__name}, indent=4)) 
        self.__read()

    def __write(self) -> None:
        with io.open(self.__path + self.__filename, 'w') as handle:
            handle.write(json.dumps(self.__config, indent=4))

    def __read(self) -> None:
        with io.open(self.__path + self.__filename, 'r') as handle:
            self.__config = json.loads(handle.read())

    def get(self) -> dict:
        """ Get the config as `dict` type """
        return self.__config

    def add(self, key: str, data: Union[List, str]) -> bool:
        """ Add data `List` or `str` to key: `str` """
        if key in dict.keys(self.__config):
            self.__config[key].append(data)
            self.__write()
            return True
        else:
            return False
    
    def set(self, key: str, data: Union[List, str]) -> bool:
        """ Set key: `str` -> data: `List` or `str` """
        if key in dict.keys(self.__config):
            self.__config.pop(key)
        self.__config.update({key: data})
        self.__write()
        return True
    
    def remove(self, key: str, list_item: Union[List[str], int, str] = None) -> bool:
        """ Removes key if not list_item """
        if key in dict.keys(self.__config):
            if list_item == None:
                self.__config.pop(key)
            elif (list_item == int or str):
                try:
                    self.__config[key].pop(list_item)
                except:
                    return False
            self.__write()
            return True
        else:
            return False
