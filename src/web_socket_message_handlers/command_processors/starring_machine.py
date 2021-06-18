from typing import Optional, List, Callable

from src.bot_controller import AbstractBotController, BotController
from src.room_state import AbstractRoomState, RoomState


class StarringMachine:
    def __init__(self, ack_word: str, bot_controller: AbstractBotController = BotController.get_instance(),
                 room_state: AbstractRoomState = RoomState.get_instance()):
        self.__current_track: Optional[dict] = None
        self.__voter_ids: List[str] = []
        self.__ack_word = ack_word
        self.__bot_controller = bot_controller
        self.__room_state = room_state

    def vote(self, user_id: str, success_action: Callable[[AbstractBotController], None]) -> None:
        if not self.__room_state.current_track:
            return
        if self.__room_state.djs[0]['id'] == user_id:
            return self.__bot_controller.chat('You can\'t vote for yourself')
            
        if self.__bot_controller.starred:
            return self.__bot_controller.chat('I\'m already starred this')
        if self.__current_track is None or self.__current_track['id'] != self.__room_state.current_track['id']:
            self.__current_track = self.__room_state.current_track
            self.__voter_ids = []
        if user_id in self.__voter_ids:
            return self.__bot_controller.chat('You\'ve already voted to star this')
        self.__voter_ids.append(user_id)
        voter_count = len(self.__voter_ids)
        if voter_count <= 2:
            self.__bot_controller.chat(', '.join(self.__ack_word for _ in range(voter_count)))
        elif voter_count == 3:
            success_action(self.__bot_controller)
