import os, io, json 
from typing import List, Tuple, Union
from abc import ABC, abstractmethod
from src.helpers import get_config_path

class AbstractConfiguration(ABC):
    @abstractmethod
    def get(self, key: str = None):
        pass

    @abstractmethod
    def update(self, key: str = None):
        pass

    @abstractmethod
    def add(self, key: str, data: Union[List, str]) -> bool:
        pass

    @abstractmethod
    def set(self, key: str, data: Union[List, int, str, bool]) -> bool:
        pass

    @abstractmethod
    def remove(self, key: str, list_item: Union[int, str] = None) -> bool:
        pass

class Configuration(AbstractConfiguration):
    def __init__(self, name: str) -> None:
        self.__name = name
        self.__path = get_config_path()
        self.__filename = self.__name + '.json'
        self.__config = dict
        if not self.__path.endswith(os.sep):
            self.__path += os.sep 
        if not os.path.exists(self.__path):
            os.mkdir(self.__path)
        if not os.path.isfile(self.__path + "/" + self.__filename):
            self.__init_config()
        self.__read()
            
    def __init_config(self) -> None:
        init_conf = {'module_name': self.__name}
        with io.open(self.__path + self.__filename, 'w') as handle:
            handle.write(json.dumps(init_conf, indent=4)) 
        self.__read()

    def __write(self) -> None:
        with io.open(self.__path + self.__filename, 'w') as handle:
            handle.write(json.dumps(self.__config, indent=4))

    def __read(self) -> None:
        with io.open(self.__path + self.__filename, 'r') as handle:
            self.__config = json.loads(handle.read())

    def get(self, key: str = None):
        """ Get the config as `dict` type if key in not defined"""
        if key == None:
            return self.__config
        return self.__config.get(key)
    
    def update(self, key: str = None):
        self.__read()
        if key == None:
            return self.__config
        return self.__config.get(key)

    def add(self, key: str, data: Union[List, str]) -> bool:
        self.__read()
        """ Add data `list` or `str` to key: `str` """
        if key in dict.keys(self.__config):
            self.__config[key].append(data)
            self.__write()
            return True
        else:
            return False
    
    def set(self, key: str, data: Union[List, int, str, bool]) -> bool:
        """ Set key: `str` -> data: `List` or `str` """
        self.__read()
        if key in dict.keys(self.__config):
            self.__config.pop(key)
        self.__config.update({key: data})
        self.__write()
        return True
    
    def remove(self, key: str, list_item: Union[List[str], int, str] = None) -> bool:
        """ Removes key if not list_item """
        self.__read()
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
