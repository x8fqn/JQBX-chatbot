from typing import Optional, List

from time import sleep

from src.bot_controller import AbstractBotController, BotController
from src.room_state import AbstractRoomState, RoomState
from src.web_socket_message_handlers.command_processors.abstract_command_processor import AbstractCommandProcessor
from src.jqbx_api import AbstractJQBXAPI, JQBXAPI


class TopRoomsProcessor(AbstractCommandProcessor):
    def __init__(self, room_state: AbstractRoomState = RoomState.get_instance(),
                 bot_controller: AbstractBotController = BotController.get_instance(),
                 jqbx_api: AbstractJQBXAPI = JQBXAPI()):
        self.__room_state = room_state
        self.__bot_controller = bot_controller
        self.__api = jqbx_api

    @property
    def keyword(self) -> str:
        return 'top'

    @property
    def help(self) -> str:
        return '''
            Top of active rooms in JQBX 
        '''

    def process(self, user_id: str, args: Optional[List[str]]) -> None:
        topRoomsReq = self.__api.roomsActive()
        respLen = 10 if len(topRoomsReq['rooms']) >= 10 else len(topRoomsReq['rooms'])
        msg = ['%s) [%s users] %s ' % (x + 1, len(topRoomsReq['rooms'][x]['users']), topRoomsReq['rooms'][x]['title']) for x in range(len(topRoomsReq['rooms']))][0:respLen]
        self.__args_processor(args, msg)

    def __args_processor(self, args: Optional[List[str]], messages: Optional[List[str]]):
        if 'mobile' and 'list' in args:
            for item in messages:
                self.__bot_controller.chat(item)
                sleep(0.1)
        elif 'list' in args:
            self.__bot_controller.chat(messages)
        else:
            self.__bot_controller.chat('; '.join(messages))


