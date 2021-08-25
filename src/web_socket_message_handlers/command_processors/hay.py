from typing import Optional, List

import json, requests
from requests.api import request
from requests.models import Response

from src.bot_controller import AbstractBotController, BotController
from src.room_state import AbstractRoomState, RoomState
from src.web_socket_message_handlers.command_processors.abstract_command_processor import AbstractCommandProcessor
from src.web_socket_message_handlers.objects.user_input import UserInput
from src.web_socket_message_handlers.objects.push_message import PushMessage


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

    def process(self, pushMessage: PushMessage, userInput: UserInput) -> None:
        room_input = userInput.args_get(0)
        message = userInput.args_getRange(1)
        if room_input and message:
            message_username = '%s (%s)' % (pushMessage.user.username, self.__room_state.room_title)
            room_id_request = json.loads(requests.get('https://jqbx.fm/rooms/search/title/%s/0' % room_input).text)

            if room_id_request['total'] == 1:
                self.__bot_controller.interroom_chat(room_id_request['rooms'][0]['_id'], message_username, message)
                self.__bot_controller.chat(':email::white_check_mark: Sent to a room called "%s" with %s users' % (
                    room_id_request['rooms'][0]['title'], str(len(room_id_request['rooms'][0]['users']))))
            elif room_id_request['total'] > 1:
                self.__bot_controller.chat(':email::x: So many rooms with that name')
            elif room_id_request['total'] <= 0:
                if len(room_input) > 23:
                    self.__bot_controller.interroom_chat(room_input, message_username, message)
                    self.__bot_controller.chat(':email::id: Sending by room ID')
                else:
                    self.__bot_controller.chat(':email::id::x: Room ID is invalid')
        else:
            self.__bot_controller.chat(':email::x: Not enough arguments')
