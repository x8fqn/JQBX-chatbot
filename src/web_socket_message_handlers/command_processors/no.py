from src.web_socket_message_handlers.command_processors.abstract_command_processor import AbstractCommandProcessor
from src.web_socket_message_handlers.command_processors.workers.voting_machine import VotingMachine
from src.web_socket_message_handlers.objects.user_input import UserInput
from src.web_socket_message_handlers.objects.push_message import PushMessage
from src.command_controller import AbstractCommandController
from src.bot_controller import AbstractBotController
from src.command_controller import AbstractCommandController
from src.room_state import AbstractRoomState
from src.settings import AbstractSettings


class NockOutCommandProcessor(AbstractCommandProcessor):
    @property
    def keyword(self) -> str:
        return 'no'

    @property
    def help(self) -> str:
        return '''
            Votes for the bot to downvote (nope) a song. Requires 3 people.
        '''

    def process(self, pushMessage: PushMessage, userInput: UserInput,
    bot_controller: AbstractBotController, room_state: AbstractRoomState, settings: AbstractSettings, command_controller: AbstractCommandController) -> None:
        self.__voting_machine = VotingMachine('no', bot_controller, room_state)
        self.__voting_machine.vote(pushMessage.user.id, self.__nope)

    def __nope(self, bot_controller: AbstractBotController) -> None:
        bot_controller.nope()
        bot_controller.chat('no, no, no :-1: no way José!')
