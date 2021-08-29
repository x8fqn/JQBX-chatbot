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
        if pushMessage.user is None or pushMessage.user.id == self.__settings.user_id: 
            isUserValid = False
        else: 
            isUserValid = True
        # Message validation
        if not (pushMessage.message.startswith(trigger_char) and len(pushMessage.message) > 1):
            isMessageValid = False
        else: 
            isMessageValid = True
        return isUserValid and isMessageValid
        