from typing import Optional, List

import json, requests
from requests.api import request
from requests.models import Response

from bot_controller import AbstractBotController, BotController
from room_state import AbstractRoomState, RoomState
from web_socket_message_handlers.command_processors.abstract_command_processor import AbstractCommandProcessor


class HayProcessor(AbstractCommandProcessor):
    def __init__(self, room_state: AbstractRoomState = RoomState.get_instance(),
                 bot_controller: AbstractBotController = BotController.get_instance()):
        self.__room_state = room_state
        self.__bot_controller = bot_controller

    @property
    def keyword(self) -> str:
        return 'hay'

    @property
    def help(self) -> str:
        return '''
            Interroom messaging. Using: /hay [roomHandle or roomID] [message]
        '''

    def process(self, user_id: str, payload: Optional[str] = None) -> None:
        if payload in {'', None}:
            return self.__bot_controller.chat('[Hay] :email::x: Not enough arguments')
        else:
            args = payload.split(' ', 1)
            if len(args) <= 1:
                return self.__bot_controller.chat('[Hay] :email::x: Not enough arguments')
        room_id = args[0]
        room_id_req = json.loads(requests.get('https://jqbx.fm/rooms/search/title/%s/0' % room_id).text)
        user_id_req = json.loads(requests.get('https://jqbx.fm/user/spotify:user:%s' % user_id).text)
        
        username_str = '%s (%s)' % (user_id_req['username'], self.__room_state.room_title)
        msg = args[1]
            
        if room_id_req['total'] == 1:
            self.__bot_controller.interroom_chat(room_id_req['rooms'][0]['_id'], username_str, msg)
            self.__bot_controller.chat('[Hay] :email::white_check_mark: Sent to a room called "%s" with %s users' % (
                room_id_req['rooms'][0]['title'], str(len(room_id_req['rooms'][0]['users']))))
            return
        if room_id_req['total'] > 1:
            self.__bot_controller.chat('[Hay] :email::x: So many rooms with that name')
            return
        elif room_id_req['total'] <= 0:
            if len(room_id) > 23:
                self.__bot_controller.interroom_chat(room_id, username_str, msg)
                self.__bot_controller.chat('[Hay] :email::id: Trying to send by room ID')
            else:
                self.__bot_controller.chat('[Hay] :email::id::x: Room ID is invalid')
            return


