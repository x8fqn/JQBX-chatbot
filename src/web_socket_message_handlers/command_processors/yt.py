from typing import Optional, List

import json
from youtube_search import YoutubeSearch as youtubeSearch

from src.bot_controller import AbstractBotController, BotController
from src.room_state import AbstractRoomState, RoomState
from src.web_socket_message_handlers.command_processors.abstract_command_processor import AbstractCommandProcessor


class YtCommandProcessor(AbstractCommandProcessor):
    def __init__(self, room_state: AbstractRoomState = RoomState.get_instance(),
                 bot_controller: AbstractBotController = BotController.get_instance()):
        self.__room_state = room_state
        self.__bot_controller = bot_controller

    @property
    def keyword(self) -> str:
        return 'yt'

    @property
    def help(self) -> str:
        return '''
            Listen to this tune on YouTube 
        '''

    def process(self, user_id: str, payload: Optional[str] = None) -> None:
        query = ''
        result = ''
        for artist in self.__room_state.current_track["artists"]:
            query += '"' + artist['name'] + '" '
        query += '"' + self.__room_state.current_track['name'] + '"'

        youtubeRequest = json.loads(
            youtubeSearch(query, max_results=10).to_json())

        durationOrig = int(
            self.__room_state.current_track['duration_ms']) // 1000

        for video in youtubeRequest['videos']:
            duration = video['duration'].split(':')
            if len(duration) > 2:
                duration = int(duration[0]) * 120 + \
                    int(duration[1]) * 60 + int(duration[2])
            elif len(duration) == 2:
                duration = int(duration[0]) * 60 + int(duration[1])
            if -2 <= (duration - durationOrig) <= 2:
                result = ['Title: %s' % video['title'], 
                          'Link: https://youtu.be/%s' % video['id'], 
                          'Duration: %s' % video['duration']]
                break
                pass
        self.__bot_controller.chat(result)
