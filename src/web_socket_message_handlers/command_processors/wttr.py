from urllib.parse import quote
from src.web_socket_message_handlers.command_processors.abstract_command_processor import AbstractCommandProcessor
from src.web_socket_message_handlers.objects.user_input import UserInput
from src.web_socket_message_handlers.objects.push_message import PushMessage
from src.command_controller import AbstractCommandController
from src.bot_controller import AbstractBotController
from src.command_controller import AbstractCommandController
from src.room_state import AbstractRoomState
from src.settings import AbstractSettings


class WttrCommandProcessor(AbstractCommandProcessor):
    @property
    def keyword(self) -> str:
        return 'wttr'

    @property
    def help(self) -> str:
        return '''
            Display the weather
        '''

    def process(self, pushMessage: PushMessage, userInput: UserInput,
    bot_controller: AbstractBotController, room_state: AbstractRoomState, settings: AbstractSettings, command_controller: AbstractCommandController) -> None:
        url = 'http://wttr.in/%s_q0np.png' % (quote(userInput.text if userInput.text else ''))
        bot_controller.chat(url)


