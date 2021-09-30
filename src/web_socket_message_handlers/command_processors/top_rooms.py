from typing import Optional, List
from src.web_socket_message_handlers.command_processors.abstract_command_processor import AbstractCommandProcessor
from src.jqbx_api import AbstractJQBXAPI, JQBXAPI
from src.web_socket_message_handlers.objects.user_input import UserInput
from src.web_socket_message_handlers.objects.push_message import PushMessage
from src.command_controller import AbstractCommandController
from src.bot_controller import AbstractBotController
from src.command_controller import AbstractCommandController
from src.room_state import AbstractRoomState
from src.settings import AbstractSettings


class TopRoomsProcessor(AbstractCommandProcessor):
    def __init__(self, jqbx_api: AbstractJQBXAPI = JQBXAPI()):
        self.__api = jqbx_api

    @property
    def keyword(self) -> str:
        return 'top'

    @property
    def help(self) -> str:
        return '''
            Top of active rooms in JQBX 
        '''

    def process(self, pushMessage: PushMessage, userInput: UserInput,
    bot_controller: AbstractBotController, room_state: AbstractRoomState, settings: AbstractSettings, command_controller: AbstractCommandController) -> None:
        topRoomsReq = self.__api.roomsActive()
        respLen = 10 if len(topRoomsReq['rooms']) >= 10 else len(topRoomsReq['rooms'])
        msg = ['%s) [%s users] %s ' % (x + 1, len(topRoomsReq['rooms'][x]['users']), topRoomsReq['rooms'][x]['title']) for x in range(len(topRoomsReq['rooms']))][0:respLen]
        self.__args_processor(userInput.arguments, msg, bot_controller)

    def __args_processor(self, args: Optional[List[str]], messages: Optional[List[str]], bot_controller: AbstractBotController):
        if args: 
            if 'nobr' in args:
                bot_controller.chat('\n'.join(messages))
            else:
                bot_controller.chat(messages)
        else: 
            bot_controller.chat(messages)

