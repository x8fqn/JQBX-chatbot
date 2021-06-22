from typing import List

from web_socket_message_handlers.command_processors.abstract_command_processor import AbstractCommandProcessor
from web_socket_message_handlers.command_processors.choose import ChooseCommandProcessor
from web_socket_message_handlers.command_processors.dadjoke import DadjokeCommandProcessor
# from web_socket_message_handlers.command_processors.no import NockOutCommandProcessor
# from web_socket_message_handlers.command_processors.relink import RelinkCommandProcessor
from web_socket_message_handlers.command_processors.ro import RockOutCommandProcessor
# from web_socket_message_handlers.command_processors.theme import ThemeCommandProcessor
from web_socket_message_handlers.command_processors.urban import UrbanCommandProcessor
from web_socket_message_handlers.command_processors.charlixcx import CharlixcxCommandProcessor
from web_socket_message_handlers.command_processors.yt import YtCommandProcessor
from web_socket_message_handlers.command_processors.star import StarProcessor
from web_socket_message_handlers.command_processors.first import FirstProcessor, AutoFirstProcessor
from web_socket_message_handlers.command_processors.hay import HayProcessor
from web_socket_message_handlers.command_processors.top_rooms import TopRoomsProcessor
from web_socket_message_handlers.command_processors.config import ConfigProcessor


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
    ConfigProcessor()
    # ThemeCommandProcessor(),
    # RelinkCommandProcessor()
]
