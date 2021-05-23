from typing import Optional, List

import json, requests

from src.bot_controller import AbstractBotController, BotController
from src.room_state import AbstractRoomState, RoomState
from src.web_socket_message_handlers.command_processors.abstract_command_processor import AbstractCommandProcessor


class TopRoomsProcessor(AbstractCommandProcessor):
    def __init__(self, room_state: AbstractRoomState = RoomState.get_instance(),
                 bot_controller: AbstractBotController = BotController.get_instance()):
        self.__room_state = room_state
        self.__bot_controller = bot_controller

    @property
    def keyword(self) -> str:
        return 'top'

    @property
    def help(self) -> str:
        return '''
            Top of active rooms in JQBX 
        '''

    def process(self, user_id: str, payload: Optional[str] = None) -> None:
        topRoomsReq = requests.get('https://jqbx.fm/active-rooms/0').json()
        respLen = 10 if len(topRoomsReq['rooms']) >= 10 else len(topRoomsReq['rooms'])
        msg = ['%s) [%s users] %s ' % (x + 1, len(topRoomsReq['rooms'][x]['users']), topRoomsReq['rooms'][x]['title']) for x in range(len(topRoomsReq['rooms']))][0:respLen]
        if payload != None:
            if payload in {'--list', '-l'}:
                return self.__bot_controller.chat(msg)    
        return self.__bot_controller.chat(', '.join(msg))


