from typing import Optional, List, cast
import requests
import json
from dateutil import parser as dateparser
from src.env import AbstractEnvironment, Environment

from src.bot_controller import AbstractBotController, BotController
from src.room_state import AbstractRoomState, RoomState
from src.web_socket_message_handlers.command_processors.abstract_command_processor import AbstractCommandProcessor

class FirstProcessor(AbstractCommandProcessor):
    def __init__(self, bot_controller: AbstractBotController = BotController.get_instance(),
                 room_state: AbstractRoomState = RoomState.get_instance(), 
                 env: AbstractEnvironment = Environment()):
        self.__bot_controller = bot_controller
        self.__room_state = room_state
        self.__env = env

    @property
    def keyword(self) -> str:
        return 'first'

    @property
    def help(self) -> str:
        return 'Get info about the first play of the current track on JQBX'

    def process(self, user_id: str, payload: Optional[str]) -> None:
        jqbx_first_request = json.loads(requests.get('%s/%s' % (
            self.__env.get_jqbx_first_api(),
            self.__room_state.current_track['uri'])).text)
        msg = ['%s by %s was first played on JQBX by "%s" on %s in "%s".' % (
                jqbx_first_request['track']['name'],
                ", ".join([i['name'] for i in jqbx_first_request['track']['artists']]),
                jqbx_first_request['user']['username'],
                dateparser.parse(jqbx_first_request['track']['startedAt']).strftime("%m/%d/%Y %H:%M"),
                jqbx_first_request['room']['title']),
            'It got %s upvote, %s stars, and %s lames.' % (
                str(jqbx_first_request['track']['thumbsUp']) if 'thumbsUp' in jqbx_first_request['track'] else '0',
                str(jqbx_first_request['track']['stars']) if 'stars' in jqbx_first_request['track'] else '0',
                str(jqbx_first_request['track']['thumbsDown']) if 'thumbsDown' in jqbx_first_request['track'] else '0'
            )]
        self.__bot_controller.chat(msg)
