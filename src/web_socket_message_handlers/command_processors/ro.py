from typing import Optional

from bot_controller import AbstractBotController
# from data_service import DataService, AbstractDataService
from room_state import AbstractRoomState, RoomState
from web_socket_message_handlers.command_processors.abstract_command_processor import AbstractCommandProcessor
from modules.voting_machine import VotingMachine


class RockOutCommandProcessor(AbstractCommandProcessor):
    def __init__(self, room_state: AbstractRoomState = RoomState.get_instance()):
        self.__voting_machine = VotingMachine('row')
        self.__room_state = room_state

    @property
    def keyword(self) -> str:
        return 'ro'

    @property
    def help(self) -> str:
        return '''
            Votes for the bot to rock out (dope) a song. Requires 3 people.
        '''

    def process(self, user_id: str, payload: Optional[str] = None) -> None:
        self.__voting_machine.vote(user_id, self.__dope_and_add_to_playlist)

    def __dope_and_add_to_playlist(self, bot_controller: AbstractBotController) -> None:
        bot_controller.dope()
        bot_controller.chat('row, row, row your :canoe: gently down the stream!')
#        playlist_id = self.__data_service.add_to_favorites_playlist(self.__room_state.current_track['id'])
#        bot_controller.chat('This track has been added to https://open.spotify.com/playlist/%s' % playlist_id)
