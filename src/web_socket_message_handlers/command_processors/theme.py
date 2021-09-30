from src.web_socket_message_handlers.command_processors.abstract_command_processor import AbstractCommandProcessor
from src.web_socket_message_handlers.objects.user_input import UserInput
from src.web_socket_message_handlers.objects.push_message import PushMessage
from src.command_controller import AbstractCommandController
from src.bot_controller import AbstractBotController
from src.command_controller import AbstractCommandController
from src.room_state import AbstractRoomState
from src.settings import AbstractSettings


class ThemeCommandProcessor(AbstractCommandProcessor):
    @property
    def keyword(self) -> str:
        return 'theme'

    @property
    def help(self) -> str:
        return '''
            See the current theme
        '''

    def process(self, pushMessage: PushMessage, userInput: UserInput,
    bot_controller: AbstractBotController, room_state: AbstractRoomState, settings: AbstractSettings, command_controller: AbstractCommandController) -> None:
        # current_welcome_message = data_service.get_welcome_message()
        # if current_welcome_message:
            # bot_controller.chat(current_welcome_message)
        # else:
            # bot_controller.chat('The theme is not currently set.')
        pass
