import json
import traceback
from datetime import datetime
from abc import ABC, abstractmethod
from typing import Union, Optional
from src.env import Environment, AbstractEnvironment

# https://datatracker.ietf.org/doc/html/rfc5424#section-6.2.1
# Levels:
#   0 - Emergency:      system is unusable
#   1 - Alert:          action must be taken immediately
#   2 - Critical:       critical conditions
#   3 - Error:          error conditions
#   4 - Warning:        warning conditions
#   5 - Notice:         normal but significant condition
#   6 - Informational:  informational messages
#   7 - Debug:          debug-level messages 

class AbstractLogger(ABC):
    @abstractmethod
    def alert(self, context: str) -> None:
        pass

    @abstractmethod
    def error(self, exception: BaseException) -> None:
        pass

    @abstractmethod
    def info(self, context: str, data: Optional[Union[str, dict, list]] = None) -> None:
        pass
    
    @abstractmethod
    def debug(self, context: str, data: Optional[Union[str, dict, list]] = None) -> None:
        pass

class Logger(AbstractLogger):
    def __init__(self, env: AbstractEnvironment = Environment()) -> None:
        self.__levels = (
            'EMERGENCY',
            'ALERT',
            'CRITICAL',
            'ERROR',
            'WARNING',
            'NOTICE',
            'INFORMATIONAL',
            'DEBUG' 
        )
        self.__envlevel = int(env.get_log_level())
        
    def debug(self, context: str, data: Optional[Union[str, dict, list]] = None) -> None:
        __level = 7
        __dateTimeString = datetime.now().strftime("%H:%M:%S %d/%m/%Y")
        if __level <= self.__envlevel:
            log = {
                'time': __dateTimeString,
                'level': self.__levels[__level],
                'context': context
            }
            if data:
                log['data'] = data
            print(json.dumps(log))
        
    def info(self, context: str, data: Optional[Union[str, dict, list]] = None) -> None:
        __level = 6
        __dateTimeString = datetime.now().strftime("%H:%M:%S %d/%m/%Y")
        if __level <= self.__envlevel:
            log = {
                'time': __dateTimeString,
                'level': self.__levels[__level],
                'context': context
            }
            if data:
                log['data'] = data
            print(json.dumps(log))

    def error(self, exception: BaseException) -> None:
        __level = 3
        __dateTimeString = datetime.now().strftime("%H:%M:%S %d/%m/%Y")
        if __level <= self.__envlevel:
            print(json.dumps({
                'time': __dateTimeString,
                'level': self.__levels[__level],
                'error': str(exception),
                'trace': traceback.format_tb(exception.__traceback__)
            }))

    def alert(self, context: str) -> None:
        __level = 1
        __dateTimeString = datetime.now().strftime("%H:%M:%S %d/%m/%Y")
        if __level <= self.__envlevel:
            log = {
                'time': __dateTimeString,
                'level': self.__levels[__level],
                'context': context
            }
            print(json.dumps(log))

