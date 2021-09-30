from src.web_socket_message_handlers.command_processors.abstract_command_processor import AbstractCommandProcessor
from src.web_socket_message_handlers.command_processors.workers.voting_machine import VotingMachine
from src.web_socket_message_handlers.objects.user_input import UserInput
from src.web_socket_message_handlers.objects.push_message import PushMessage
from src.command_controller import AbstractCommandController
from src.bot_controller import AbstractBotController
from src.command_controller import AbstractCommandController
from src.room_state import AbstractRoomState
from src.settings import AbstractSettings

class RockOutCommandProcessor(AbstractCommandProcessor):
    @property
    def keyword(self) -> str:
        return 'ro'

    @property
    def help(self) -> str:
        return '''
            Votes for the bot to rock out (dope) a song. Requires 3 people.
        '''

    def process(self, pushMessage: PushMessage, userInput: UserInput,
    bot_controller: AbstractBotController, room_state: AbstractRoomState, settings: AbstractSettings, command_controller: AbstractCommandController) -> None:
        try:
            self.__voting_machine.vote(pushMessage.user.id, self.__dope_and_add_to_playlist)
        except:
            self.__voting_machine = VotingMachine('row', bot_controller, room_state)
            self.__voting_machine.vote(pushMessage.user.id, self.__dope_and_add_to_playlist)

    def __dope_and_add_to_playlist(self, bot_controller: AbstractBotController) -> None:
        bot_controller.dope()
        bot_controller.chat('row, row, row your :canoe: gently down the stream!')
#        playlist_id = self.__data_service.add_to_favorites_playlist(self.__room_state.current_track['id'])
#        bot_controller.chat('This track has been added to https://open.spotify.com/playlist/%s' % playlist_id)
