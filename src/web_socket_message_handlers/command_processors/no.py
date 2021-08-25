from typing import Optional, List

from src.bot_controller import AbstractBotController
from src.web_socket_message_handlers.command_processors.abstract_command_processor import AbstractCommandProcessor
from src.web_socket_message_handlers.command_processors.workers.voting_machine import VotingMachine
from src.web_socket_message_handlers.objects.user_input import UserInput
from src.web_socket_message_handlers.objects.push_message import PushMessage


class NockOutCommandProcessor(AbstractCommandProcessor):
    def __init__(self):
        self.__voting_machine = VotingMachine('no')

    @property
    def keyword(self) -> str:
        return 'no'

    @property
    def help(self) -> str:
        return '''
            Votes for the bot to downvote (nope) a song. Requires 3 people.
        '''

    def process(self, pushMessage: PushMessage, userInput: UserInput) -> None:
        self.__voting_machine.vote(pushMessage.user.id, self.__nope)

    def __nope(self, bot_controller: AbstractBotController) -> None:
        bot_controller.nope()
        bot_controller.chat('no, no, no :-1: no way José!')
