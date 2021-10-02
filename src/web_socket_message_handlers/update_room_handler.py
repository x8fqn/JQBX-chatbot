from typing import List
from src.web_socket_message_handlers.abstract_web_socket_message_handler import AbstractWebSocketMessageHandler
from src.web_socket_message import WebSocketMessage
from src.core import Core


class UpdateRoomHandler(AbstractWebSocketMessageHandler):
    def __init__(self):
        pass

    @property
    def message_label(self) -> str:
        return 'update-room'

    def handle(self, message: WebSocketMessage, core: Core) -> None:
        payload = message.payload
        self.__update_mod_ids(payload, core)
        self.__update_users(payload, core)
        self.__update_room_title(payload, core)
        self.__update_votes(payload, core)
        self.__initial_track_update(payload, core)

    def __update_mod_ids(self, payload: dict, core: Core) -> None:
        admins = payload.get('admin', [])
        mods = payload.get('mods', [])
        if admins + mods:
            core.room_state.set_mod_ids([x.split(':')[-1] for x in list(set(admins + mods))])

    def __update_users(self, payload: dict, core: Core) -> None:
        users: List[dict] = payload.get('users', [])
        djs: List[dict] = payload.get('djs', [])
        if core.room_state.users:
            new_users = [
                user for user in users
                if user['id'] != core.settings.user_id
                   and user['id'] not in [y['id'] for y in core.room_state.users]
            ]

        if 'new_users' in locals():
            if core.settings.welcome_isEnabled:
                for user in new_users:
                    if core.settings.welcome_isWhisper:
                        core.bot_controller.whisper(core.settings.welcome_message, user)
                    else:
                        core.bot_controller.chat(core.settings.welcome_message)

        if 'users' in payload:
            core.room_state.set_users(users)

        if 'djs' in payload:
            core.room_state.set_djs(djs)

    def __initial_track_update(self, payload: dict, core: Core) -> None:
        tracks = payload.get('tracks', [])
        if tracks:
            core.room_state.set_current_track(tracks[0])

    def __update_room_title(self, payload: dict, core: Core) -> None:
        room_title = payload.get('title')
        if room_title:
            core.room_state.set_room_title(room_title)

    def __update_votes(self, payload: dict, core: Core) -> None:
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
        core.room_state.set_votes(thumbUp_count, thumbDown_count, star_count, core.room_state.max_user_count)
