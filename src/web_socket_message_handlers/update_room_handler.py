import os
from typing import List

from src.bot_controller import AbstractBotController, BotController
from src.settings import AbstractSettings, Settings
from src.room_state import AbstractRoomState, RoomState
from src.web_socket_message import WebSocketMessage
from src.web_socket_message_handlers.abstract_web_socket_message_handler import AbstractWebSocketMessageHandler


class UpdateRoomHandler(AbstractWebSocketMessageHandler):
    def __init__(self, bot_controller: AbstractBotController = BotController.get_instance(),
                 room_state: AbstractRoomState = RoomState.get_instance(),
                 settings: AbstractSettings = Settings.get_instance()):
        self.__bot_controller = bot_controller
        self.__room_state = room_state
        self.__settings = settings

    @property
    def message_label(self) -> str:
        return 'update-room'

    def handle(self, message: WebSocketMessage) -> None:
        payload = message.payload
        self.__update_mod_ids(payload)
        self.__update_users(payload)
        self.__update_room_title(payload)
        self.__initial_track_update(payload)
        self.__update_votes(payload)

    def __update_mod_ids(self, payload: dict) -> None:
        admins = payload.get('admin', [])
        mods = payload.get('mods', [])
        if admins + mods:
            self.__room_state.set_mod_ids([x.split(':')[-1] for x in list(set(admins + mods))])

    def __update_users(self, payload: dict) -> None:
        users: List[dict] = payload.get('users', [])
        djs: List[dict] = payload.get('djs', [])
        if self.__room_state.users:
            new_users = [
                user for user in users
                if user['id'] != self.__settings.user_id
                   and user['id'] not in [y['id'] for y in self.__room_state.users]
            ]

        if 'new_users' in locals():
            if self.__settings.welcome_isEnabled:
                for user in new_users:
                    if self.__settings.welcome_isWhisper:
                        self.__bot_controller.whisper(self.__settings.welcome_message, user)
                    else:
                        self.__bot_controller.chat(self.__settings.welcome_message)

        if 'users' in payload:
            self.__room_state.set_users(users)

        if 'djs' in payload:
            self.__room_state.set_djs(djs)

    def __initial_track_update(self, payload: dict) -> None:
        tracks = payload.get('tracks', [])
        if tracks:
            self.__room_state.set_current_track(tracks[0])

    def __update_room_title(self, payload: dict) -> None:
        room_title = payload.get('title')
        if room_title:
            self.__room_state.set_room_title(room_title)

    def __update_votes(self, payload: dict) -> None:
        if 'currentTrack' not in payload.keys():
            return
        payload = payload.get('currentTrack')
        thumbUp_count = payload.get('thumbsUp')
        thumbDown_count = payload.get('thumbsDown')
        star_count = payload.get('stars')
        if not thumbUp_count:
            thumbUp_count = 0
        if not thumbDown_count:
            thumbDown_count = 0
        if not star_count:
            star_count = 0
        self.__room_state.set_votes(thumbUp_count, thumbDown_count, star_count, self.__room_state.max_user_count)
