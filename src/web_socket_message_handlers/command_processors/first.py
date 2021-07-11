import requests, json
from typing import Optional, List
from dateutil import parser as dateparser

from src.jqbx_api import AbstractJQBXAPI, JQBXAPI
from src.bot_controller import AbstractBotController, BotController
from src.room_state import AbstractRoomState, RoomState
from src.web_socket_message_handlers.command_processors.abstract_command_processor import AbstractCommandProcessor
from src.config import AbstractConfig, Config

class FirstProcessor(AbstractCommandProcessor):
    def __init__(self, bot_controller: AbstractBotController = BotController.get_instance(),
                 room_state: AbstractRoomState = RoomState.get_instance(),
                 jqbx_api: AbstractJQBXAPI = JQBXAPI()):
        self.__bot_controller = bot_controller
        self.__room_state = room_state
        self.__api = jqbx_api

    @property
    def keyword(self) -> str:
        return 'first'

    @property
    def help(self) -> str:
        return 'Get info about the first play of the current track on JQBX'

    def process(self, user_id: str, payload: Optional[List[str]]) -> None:
        jqbx_first_request = self.__api.firsts(self.__room_state.current_track['uri'])
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
        if user_id == str(jqbx_first_request['user']['uri']).replace('spotify:user:',''):
            msg.insert(0, ':cake:')
        self.__bot_controller.chat(' '.join(msg))

class AutoFirstProcessor(AbstractCommandProcessor):
    def __init__(self, bot_controller: AbstractBotController = BotController.get_instance(),
                 config: AbstractConfig = Config('bot_main')):
        self.__config = config
        self.__bot_controller = bot_controller

    @property
    def keyword(self) -> str:
        return 'auto-first'

    @property
    def help(self) -> str:
        return 'Switch auto-first on every tune'

    def process(self, user_id: str, args: Optional[str]) -> None:
        try:
            if self.__config.get()['auto-first'] == True:
                self.__config.set('auto-first', False)
                return self.__bot_controller.chat('Auto-first deactivated')
            elif self.__config.get()['auto-first'] == False:
                self.__config.set('auto-first', True)
                return self.__bot_controller.chat('Auto-first activated')
            elif self.__config.get()['auto-first'] == None:
                self.__config.set('auto-first', True)
                return self.__bot_controller.chat('Auto-first activated')
        except:
            self.__config.set('auto-first', True)
            return self.__bot_controller.chat('Auto-first activated')
