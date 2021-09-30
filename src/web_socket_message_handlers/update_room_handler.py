import os
from typing import List

from src.bot_controller import AbstractBotController, BotController
from src.command_controller import AbstractCommandController
from src.settings import AbstractSettings, Settings
from src.room_state import AbstractRoomState, RoomState
from src.web_socket_message import WebSocketMessage
from src.web_socket_message_handlers.abstract_web_socket_message_handler import AbstractWebSocketMessageHandler
from src.web_socket_client import AbstractWebSocketClient


class UpdateRoomHandler(AbstractWebSocketMessageHandler):
    def __init__(self):
        pass

    @property
    def message_label(self) -> str:
        return 'update-room'

    def handle(self, message: WebSocketMessage, web_socket_client: AbstractWebSocketClient,
    settings: AbstractSettings, bot_controller: AbstractBotController,
    room_state: AbstractRoomState, command_controller: AbstractCommandController) -> None:
        payload = message.payload
        self.__update_mod_ids(payload, room_state)
        self.__update_users(payload, room_state, settings, bot_controller)
        self.__update_room_title(payload, room_state)
        self.__update_votes(payload, room_state)
        self.__initial_track_update(payload, room_state)

    def __update_mod_ids(self, payload: dict, room_state: AbstractRoomState) -> None:
        admins = payload.get('admin', [])
        mods = payload.get('mods', [])
        if admins + mods:
            room_state.set_mod_ids([x.split(':')[-1] for x in list(set(admins + mods))])

    def __update_users(self, payload: dict, room_state: AbstractRoomState, settings: AbstractSettings, bot_controller: AbstractBotController) -> None:
        users: List[dict] = payload.get('users', [])
        djs: List[dict] = payload.get('djs', [])
        if room_state.users:
            new_users = [
                user for user in users
                if user['id'] != settings.user_id
                   and user['id'] not in [y['id'] for y in room_state.users]
            ]

        if 'new_users' in locals():
            if settings.welcome_isEnabled:
                for user in new_users:
                    if settings.welcome_isWhisper:
                        bot_controller.whisper(settings.welcome_message, user)
                    else:
                        bot_controller.chat(settings.welcome_message)

        if 'users' in payload:
            room_state.set_users(users)

        if 'djs' in payload:
            room_state.set_djs(djs)

    def __initial_track_update(self, payload: dict, room_state: AbstractRoomState) -> None:
        tracks = payload.get('tracks', [])
        if tracks:
            room_state.set_current_track(tracks[0])

    def __update_room_title(self, payload: dict, room_state: AbstractRoomState) -> None:
        room_title = payload.get('title')
        if room_title:
            room_state.set_room_title(room_title)

    def __update_votes(self, payload: dict, room_state: AbstractRoomState) -> None:
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
        room_state.set_votes(thumbUp_count, thumbDown_count, star_count, room_state.max_user_count)
