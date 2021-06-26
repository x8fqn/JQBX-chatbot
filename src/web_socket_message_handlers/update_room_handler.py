from typing import List

from bot_controller import AbstractBotController, BotController
from configuration import AbstractConfiguration, Configuration
from room_state import AbstractRoomState, RoomState
from web_socket_message import WebSocketMessage
from web_socket_message_handlers.abstract_web_socket_message_handler import AbstractWebSocketMessageHandler


class UpdateRoomHandler(AbstractWebSocketMessageHandler):
    def __init__(self, bot_controller: AbstractBotController = BotController.get_instance(),
                 room_state: AbstractRoomState = RoomState.get_instance()):
        self.__bot_controller = bot_controller
        self.__room_state = room_state
        self.__config: AbstractConfiguration = Configuration('bot_main', '../config')
        self.__welcome_config: AbstractConfiguration = Configuration('welcome','../config')

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
                if user['id'] != self.__config.get()['spotify_user_id']
                   and user['id'] not in [y['id'] for y in self.__room_state.users]
            ]

        if 'users' in payload:
            self.__room_state.set_users(users)

        self.__welcome_config.update()
        if self.__welcome_config.get()['enabled'] == True:
            if 'new_users' in locals():
                for user in new_users:
                    self.__bot_controller.whisper(self.__welcome_config.get()['message'], user)

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
        if 'currentTrack' not in payload.values():
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
        self.__room_state.set_votes(thumbUp_count, thumbDown_count, star_count)
