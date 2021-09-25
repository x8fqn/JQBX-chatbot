from typing import List

from src.web_socket_message_handlers.command_processors.abstract_command_processor import AbstractCommandProcessor
from src.web_socket_message_handlers.command_processors.choose import ChooseCommandProcessor
from src.web_socket_message_handlers.command_processors.dadjoke import DadjokeCommandProcessor
from src.web_socket_message_handlers.command_processors.ro import RockOutCommandProcessor
from src.web_socket_message_handlers.command_processors.no import NockOutCommandProcessor
from src.web_socket_message_handlers.command_processors.urban import UrbanCommandProcessor
from src.web_socket_message_handlers.command_processors.charlixcx import CharlixcxCommandProcessor
from src.web_socket_message_handlers.command_processors.yt import YtCommandProcessor
from src.web_socket_message_handlers.command_processors.star import StarProcessor
from src.web_socket_message_handlers.command_processors.first import FirstCommandProcessor, AutoFirstCommandProcessor
from src.web_socket_message_handlers.command_processors.hay import HayProcessor
from src.web_socket_message_handlers.command_processors.top_rooms import TopRoomsProcessor
from src.web_socket_message_handlers.command_processors.config import ConfigProcessor
from src.web_socket_message_handlers.command_processors.alias import AliasesProcessor
from src.web_socket_message_handlers.command_processors.single import SingleProcessor
from src.web_socket_message_handlers.command_processors.tv import TvCommandProcessor
from src.web_socket_message_handlers.command_processors.command import CommandCommandProcessor
from src.web_socket_message_handlers.command_processors.botchat import AlertCommandProcessor, SpeakCommandProcessor
from src.web_socket_message_handlers.command_processors.fixgif import FixGifCommandProcessor
from src.web_socket_message_handlers.command_processors.wttr import WttrCommandProcessor

class Processors:
    __command_processors: List[AbstractCommandProcessor] = [
        DadjokeCommandProcessor(),
        TvCommandProcessor(),
        RockOutCommandProcessor(),
        NockOutCommandProcessor(),
        UrbanCommandProcessor(),
        ChooseCommandProcessor(),
        CharlixcxCommandProcessor(),
        YtCommandProcessor(),
        StarProcessor(),
        FirstCommandProcessor(),
        AutoFirstCommandProcessor(),
        HayProcessor(),
        TopRoomsProcessor(),
        ConfigProcessor(),
        AliasesProcessor(),
        SingleProcessor(),
        CommandCommandProcessor(),
        AlertCommandProcessor(),
        SpeakCommandProcessor(),
        FixGifCommandProcessor(),
        WttrCommandProcessor()
    ]
    
    def __init__(self) -> None:
        self.command_processors = {x.keyword: x for x in self.__command_processors}

    def get(self, keyword: str):
        return self.command_processors.get(keyword, None)
