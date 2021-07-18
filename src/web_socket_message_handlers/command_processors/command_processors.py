from typing import List

from src.web_socket_message_handlers.command_processors.abstract_command_processor import AbstractCommandProcessor
from src.web_socket_message_handlers.command_processors.choose import ChooseCommandProcessor
from src.web_socket_message_handlers.command_processors.dadjoke import DadjokeCommandProcessor
# from web_socket_message_handlers.command_processors.no import NockOutCommandProcessor
# from web_socket_message_handlers.command_processors.relink import RelinkCommandProcessor
from src.web_socket_message_handlers.command_processors.ro import RockOutCommandProcessor
# from web_socket_message_handlers.command_processors.theme import ThemeCommandProcessor
from src.web_socket_message_handlers.command_processors.urban import UrbanCommandProcessor
from src.web_socket_message_handlers.command_processors.charlixcx import CharlixcxCommandProcessor
from src.web_socket_message_handlers.command_processors.yt import YtCommandProcessor
from src.web_socket_message_handlers.command_processors.star import StarProcessor
from src.web_socket_message_handlers.command_processors.first import FirstProcessor, AutoFirstProcessor
from src.web_socket_message_handlers.command_processors.hay import HayProcessor
from src.web_socket_message_handlers.command_processors.top_rooms import TopRoomsProcessor
from src.web_socket_message_handlers.command_processors.config import ConfigProcessor
from src.web_socket_message_handlers.command_processors.alias import AliasesProcessor


command_processors: List[AbstractCommandProcessor] = [
    DadjokeCommandProcessor(),
    RockOutCommandProcessor(),
    # NockOutCommandProcessor(),
    UrbanCommandProcessor(),
    ChooseCommandProcessor(),
    CharlixcxCommandProcessor(),
    YtCommandProcessor(),
    StarProcessor(),
    FirstProcessor(),
    AutoFirstProcessor(),
    HayProcessor(),
    TopRoomsProcessor(),
    ConfigProcessor(),
    AliasesProcessor()
    # ThemeCommandProcessor(),
    # RelinkCommandProcessor()
]
