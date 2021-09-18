import string, re
from html import unescape
from typing import Any, List, Optional, Tuple, Union

__all__ = ['UserInput']

class UserInput:
    def __init__(self, text: str, trigger_username: str, trigger_char: str = '/') -> None:
        self.__trig_char = trigger_char
        self.__original_input = text
        # Clearing username mention
        if self.__original_input.startswith(trigger_username): 
            self.__original_input = self.__original_input.replace(trigger_username, '').strip()
        # Parsing
        self.__keyword, self.__args = self.__split_input(self.__original_input, self.__trig_char)
        self.__parts = self.__original_input.split(' ', 1)

    @property
    def keyword(self) -> str:
        return self.__keyword

    @property
    def arguments(self) -> Optional[List[str]]:
        return self.__args

    @property
    def text(self) -> Optional[str]:
        if len(self.__parts) == 2:
            return self.__parts[1]
    
    def args_check(self, entry: str, pos: int = None) -> bool:
        if self.__args:
            if pos:
                if (entry in self.__args) and (self.__args.index(entry) == pos): return True
            else:
                if entry in self.__args: return True
        return False

    def args_get(self, index: int, ifNot: Any = None):
        if self.__args:
            try:
                return self.__args[index]
            except IndexError:
                return ifNot
        else:
            return ifNot
    
    def args_getRange(self, start_index: int = None, end_index: int = None, ifNot: Any = None):
        if self.__args:
            args = self.__args[start_index:end_index]
            if args != []:
                return args
        return ifNot

    def __filter(self, text: str):
        result = unescape(text.strip())
        result = ''.join([letter for letter in result if letter in string.printable])
        return result

    def __split_input(self, text: str, trigger: str) -> Tuple[Union[str, List[str]]]:
        text = self.__filter(text)
        # parsing for keyword
        pattern = '^\%s(?P<keyword>\S+)\s*(?P<args>.*)$' % (trigger,)
        match = re.search(pattern, text, re.MULTILINE | re.IGNORECASE)
        keyword = match.group('keyword')
        args = None if (match.group('args') == '') else match.group('args')
        # parsing for arguments if `args` is not None
        pattern = '(?:\"(.|[^\"]*)\")(?=\s+|\Z)|(\S+)'
        if args:
            temp_args = list()
            for x in re.finditer(pattern, args, re.MULTILINE | re.IGNORECASE):
                temp_args.append(x.group(1) or x.group(2))
            args = temp_args
        return (keyword, args)
