from src.web_socket_message_handlers.objects.user_input import UserInput
from src.web_socket_message_handlers.objects.push_message import PushMessage
from src.settings import AbstractSettings, Settings
from src.bot_controller import AbstractBotController, BotController
from src.web_socket_message_handlers.command_processors.abstract_command_processor import AbstractCommandProcessor


class TvCommandProcessor(AbstractCommandProcessor):
    def __init__(self, bot_controller: AbstractBotController = BotController.get_instance(),
    settings: AbstractSettings = Settings.get_instance()) -> None:
        self.__bot_controller = bot_controller
        self.__settings = settings       

    @property
    def keyword(self) -> str:
        return 'tv'

    @property
    def help(self) -> str:
        return 'Get JQBX TV link'

    def process(self, pushMessage: PushMessage, userInput: UserInput) -> None:
        self.__bot_controller.chat('https://tv.jqbx.fm/tv/%s' % self.__settings.room_id)
