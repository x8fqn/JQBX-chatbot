import logging
from src.room_state import AbstractRoomState, RoomState
from src.command_controller import AbstractCommandController, CommandController
from src.settings import AbstractSettings, Settings
from src.room_state import AbstractRoomState, RoomState
from src.web_socket_message_handlers.command_handler import CommandHandler
from src.web_socket_client import AbstractWebSocketClient

from .objects.push_message import PushMessage
from .objects.user_input import UserInput

from src.web_socket_message import WebSocketMessage
from src.web_socket_message_handlers.abstract_web_socket_message_handler import AbstractWebSocketMessageHandler
from src.bot_controller import AbstractBotController, BotController


class PushMessageHandler(AbstractWebSocketMessageHandler):
    def __init__(self, command_handler: CommandHandler = CommandHandler()):
        self.__command_handler = command_handler

    @property
    def message_label(self) -> str:
        return 'push-message'

    def handle(self, message: WebSocketMessage, web_socket_client: AbstractWebSocketClient,
    settings: AbstractSettings, bot_controller: AbstractBotController,
    room_state: AbstractRoomState, command_controller: AbstractCommandController) -> None:
        # Character(s) (tags), the message starts with
        trigger_username = '@' + settings.user['username']
        trigger_char = '/'
        # Payload extracting
        pushMessage = PushMessage(message)
        # Saving this message if not pm
        if not pushMessage.recipients:
            room_state.add_message(pushMessage)
        # Validation
        if self.__isValidMessage(settings, pushMessage, trigger_username, trigger_char): 
            userInput = UserInput(pushMessage.message, trigger_username, trigger_char)
            self.__command_handler.handle(userInput, pushMessage, bot_controller, room_state, settings, command_controller)

    def __isValidMessage(self, settings: AbstractSettings, pushMessage: PushMessage, trigger_username: str, trigger_char: str = '/') -> bool:
        isUserValid = True
        isMessageValid = True
        # User validation
        if pushMessage.user is None or pushMessage.user.id == settings.user_id: 
            isUserValid = False
        # Message validation
        if not ((pushMessage.message.startswith(trigger_char) or pushMessage.message.startswith(trigger_username)) and len(pushMessage.message) > 1):
            isMessageValid = False
        return isUserValid and isMessageValid
        