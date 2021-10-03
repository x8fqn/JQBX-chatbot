import requests, json
from typing import Optional, List
from dateutil import parser as dateparser

from src.jqbx_api import AbstractJQBXAPI, JQBXAPI
from src.web_socket_message_handlers.command_processors.abstract_command_processor import AbstractCommandProcessor
from src.web_socket_message_handlers.objects.user_input import UserInput
from src.web_socket_message_handlers.objects.push_message import PushMessage
from src.command_controller import AbstractCommandController
from src.bot_controller import AbstractBotController
from src.command_controller import AbstractCommandController
from src.room_state import AbstractRoomState
from src.settings import AbstractSettings


class FirstCommandProcessor(AbstractCommandProcessor):
    def __init__(self, jqbx_api: AbstractJQBXAPI = JQBXAPI()):
        self.__api = jqbx_api

    @property
    def keyword(self) -> str:
        return 'first'

    @property
    def help(self) -> str:
        return 'Get info about the first play of the current track on JQBX'

    def process(self, pushMessage: PushMessage, userInput: UserInput,
    bot_controller: AbstractBotController, room_state: AbstractRoomState, settings: AbstractSettings, command_controller: AbstractCommandController) -> None:
        jqbx_first_request = self.__api.firsts(room_state.current_track['uri'])
        firstDB = {
            'track_name': str(jqbx_first_request['track']['name']),
            'artists': ", ".join([i['name'] for i in jqbx_first_request['track']['artists']]),
            'username': jqbx_first_request['user']['username'] if 'username' in jqbx_first_request['user'] 
                    else str(jqbx_first_request['user']['uri']).replace('spotify:user:',''),
            'startedAt': dateparser.parse(jqbx_first_request['track']['startedAt']).strftime("%m/%d/%Y"),
            'room_title': jqbx_first_request['room']['title'],
            'thumbsUp': str(jqbx_first_request['track']['thumbsUp']) if 'thumbsUp' in jqbx_first_request['track'] else '0',
            'stars': str(jqbx_first_request['track']['stars']) if 'stars' in jqbx_first_request['track'] else '0',
            'thumbsDown': str(jqbx_first_request['track']['thumbsDown']) if 'thumbsDown' in jqbx_first_request['track'] else '0'
        }
        msg = ['[%s — %s] [Username: %s] [Date: %s] [Room: %s]' % (
                firstDB['track_name'], firstDB['artists'], firstDB['username'],
                firstDB['startedAt'], firstDB['room_title']),
            '[%s upvote%s, %s star%s, %s lame%s]' % (
                firstDB['thumbsUp'],
                's' if int(firstDB['thumbsUp']) % 10 != 1 else '',
                firstDB['stars'],
                's' if int(firstDB['stars']) % 10 != 1 else '',
                firstDB['thumbsDown'],
                's' if int(firstDB['thumbsDown']) % 10 != 1 else '')]

        if (room_state.djs[0]['uri'] == jqbx_first_request['user']['uri']):
            if jqbx_first_request['room']['_id'] == settings.room_id:
                msg.insert(0, ':cake:')
            else:
                msg.insert(0, ':cookie:')
        bot_controller.chat(' '.join(msg))

class AutoFirstCommandProcessor(AbstractCommandProcessor):
    @property
    def keyword(self) -> str:
        return 'auto-first'

    @property
    def help(self) -> str:
        return 'Switch "first" on every tune'

    def process(self, pushMessage: PushMessage, userInput: UserInput,
    bot_controller: AbstractBotController, room_state: AbstractRoomState, settings: AbstractSettings, command_controller: AbstractCommandController) -> None:
        if settings.autofirst_isEnabled:
            settings.autofirst_set_enable(False)
            return bot_controller.chat('Auto-first deactivated')
        else:
            settings.autofirst_set_enable(True)
            return bot_controller.chat('Auto-first activated')
