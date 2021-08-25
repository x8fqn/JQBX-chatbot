import logging
from src.command_controller import AbstractCommandController, CommandController
from src.settings import AbstractSettings, Settings
from src.web_socket_message_handlers.command_handler import CommandHandler

from .objects.push_message import PushMessage
from .objects.user_input import UserInput

from src.web_socket_message import WebSocketMessage
from src.web_socket_message_handlers.abstract_web_socket_message_handler import AbstractWebSocketMessageHandler
from src.bot_controller import AbstractBotController, BotController




class PushMessageHandler(AbstractWebSocketMessageHandler):
    def __init__(self, bot_controller: AbstractBotController = BotController.get_instance(),
    settings: AbstractSettings = Settings.get_instance(), 
    command_controller: AbstractCommandController = CommandController.get_instance(),
    command_handler = CommandHandler()):
        self.__bot_controller = bot_controller
        self.__settings = settings
        self.__command_controller = command_controller
        self.__command_handler = command_handler
        # self.__command_controller.set_keywords([self.__command_processors[key].keyword for key in self.__command_processors.keys()])

    @property
    def message_label(self) -> str:
        return 'push-message'

    def handle(self, ws_message: WebSocketMessage) -> None:
        # Character(s), the message starts with
        trigger_char = '/'
        # Payload extracting
        pushMessage = PushMessage(ws_message)
        # Validation
        if self.__isValidMessage(pushMessage, trigger_char): 
            userInput = UserInput(pushMessage.message, trigger_char)
            self.__command_handler.handle(userInput, pushMessage)


    def __isValidMessage(self, pushMessage: PushMessage, trigger_char: str = '/') -> bool:
        isUserValid = True
        isMessageValid = True
        # User validation
        if pushMessage.user.uri is None or pushMessage.user.uri == self.__settings.user_id: 
            isUserValid = False
        else: 
            isUserValid = True
        # Message validation
        if not (pushMessage.message.startswith(trigger_char) and len(pushMessage.message) > 1):
            isMessageValid = False
        else: 
            isMessageValid = True
        return isUserValid and isMessageValid

    # def __preprocess(self, command_processors: Dict[str, AbstractCommandProcessor], keyword, user_id, users_payload, command: Command = None) -> None:
    #     if command:
    #         if users_payload:
    #             if users_payload[0] == ('remove' or 'delete'):
    #                 if self.__command_controller.remove_command(command.command_id):
    #                     self.__bot_controller.chat('%s has been removed!' % command.name)
    #                 else:
    #                     self.__bot_controller.chat('%s is built-in or failed to remove' % command.name)
    #         else:
    #             if isinstance(command, Alias):
    #                 self.__process(command_processors, keyword, user_id, users_payload)
    #             elif isinstance(command, Single):
    #                 self.__bot_controller.chat(command.message)
    #     else:
    #         self.__process(command_processors, keyword, user_id, users_payload)

    # def __process(self, command_processors: Dict[str, AbstractCommandProcessor], keyword, user_id, users_payload) -> None:
    #     command_processor = command_processors.get(keyword)
    #     if command_processor:
    #             try:
    #                 command_processor.process(user_id, users_payload)
    #             except (IndexError, TypeError) as e:
    #                 logging.error(e)
    #                 self.__bot_controller.chat('Unable to process input data. Please, specify the request')
    #             except Exception as e:
    #                 logging.error(e)
    #                 self.__bot_controller.chat('An error occurred while processing the command')
        