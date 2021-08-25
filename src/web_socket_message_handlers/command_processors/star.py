from typing import Optional, List

from src.bot_controller import AbstractBotController
from src.room_state import AbstractRoomState, RoomState
from src.web_socket_message_handlers.command_processors.abstract_command_processor import AbstractCommandProcessor
from src.web_socket_message_handlers.command_processors.workers.starring_machine import StarringMachine
from src.web_socket_message_handlers.objects.user_input import UserInput
from src.web_socket_message_handlers.objects.push_message import PushMessage


class StarProcessor(AbstractCommandProcessor):
    def __init__(self, room_state: AbstractRoomState = RoomState.get_instance()):
        self.__starring_machine = StarringMachine('star')
        self.__room_state = room_state

    @property
    def keyword(self) -> str:
        return 'star'

    @property
    def help(self) -> str:
        return '''
            Votes for the bot to star a song. Requires 3 people.
        '''

    def process(self, pushMessage: PushMessage, userInput: UserInput) -> None:
        self.__starring_machine.vote(pushMessage.user.id, self.__star)

    def __star(self, bot_controller: AbstractBotController) -> None:
        bot_controller.star()
        bot_controller.chat('That big star is for you https://i.gifer.com/ZNec.gif')
