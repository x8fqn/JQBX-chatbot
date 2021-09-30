from src.web_socket_message_handlers.command_processors.abstract_command_processor import AbstractCommandProcessor
from src.web_socket_message_handlers.objects.user_input import UserInput
from src.web_socket_message_handlers.objects.push_message import PushMessage
from src.command_controller import AbstractCommandController
from src.bot_controller import AbstractBotController
from src.command_controller import AbstractCommandController
from src.room_state import AbstractRoomState
from src.settings import AbstractSettings


class TvCommandProcessor(AbstractCommandProcessor):  
    @property
    def keyword(self) -> str:
        return 'tv'

    @property
    def help(self) -> str:
        return 'Get JQBX TV link'

    def process(self, pushMessage: PushMessage, userInput: UserInput,
    bot_controller: AbstractBotController, room_state: AbstractRoomState, settings: AbstractSettings, command_controller: AbstractCommandController) -> None:
        bot_controller.chat('https://tv.jqbx.fm/tv/%s' % settings.room_id)
