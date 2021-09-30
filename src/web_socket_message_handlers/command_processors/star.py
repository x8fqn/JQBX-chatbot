from src.web_socket_message_handlers.command_processors.abstract_command_processor import AbstractCommandProcessor
from src.web_socket_message_handlers.command_processors.workers.starring_machine import StarringMachine
from src.web_socket_message_handlers.objects.user_input import UserInput
from src.web_socket_message_handlers.objects.push_message import PushMessage
from src.command_controller import AbstractCommandController
from src.bot_controller import AbstractBotController
from src.command_controller import AbstractCommandController
from src.room_state import AbstractRoomState
from src.settings import AbstractSettings

class StarProcessor(AbstractCommandProcessor):
    @property
    def keyword(self) -> str:
        return 'star'

    @property
    def help(self) -> str:
        return '''
            Votes for the bot to star a song. Requires 3 people.
        '''

    def process(self, pushMessage: PushMessage, userInput: UserInput,
    bot_controller: AbstractBotController, room_state: AbstractRoomState, settings: AbstractSettings, command_controller: AbstractCommandController) -> None:
        try:
            self.__starring_machine.vote(pushMessage.user.id, self.__star)
        except:
            self.__starring_machine = StarringMachine('star', bot_controller, room_state)
            self.__starring_machine.vote(pushMessage.user.id, self.__star)


    def __star(self, bot_controller: AbstractBotController) -> None:
        bot_controller.star()
        bot_controller.chat('That big star is for you https://i.gifer.com/ZNec.gif')
