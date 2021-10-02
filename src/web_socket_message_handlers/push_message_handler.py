from src.web_socket_message_handlers.command_handler import CommandHandler
from .objects.push_message import PushMessage
from .objects.user_input import UserInput
from src.settings import AbstractSettings
from src.web_socket_message import WebSocketMessage
from src.web_socket_message_handlers.abstract_web_socket_message_handler import AbstractWebSocketMessageHandler
from src.core import Core


class PushMessageHandler(AbstractWebSocketMessageHandler):
    def __init__(self, command_handler: CommandHandler = CommandHandler()):
        self.__command_handler = command_handler

    @property
    def message_label(self) -> str:
        return 'push-message'

    def handle(self, message: WebSocketMessage, core: Core) -> None:
        # Character(s) (tags), the message starts with
        trigger_username = '@' + core.settings.user['username']
        trigger_char = '/'
        # Payload extracting
        pushMessage = PushMessage(message)
        # Saving this message if not pm
        if not pushMessage.recipients:
            core.room_state.add_message(pushMessage)
        # Validation
        if self.__isValidMessage(core, pushMessage, trigger_username, trigger_char): 
            userInput = UserInput(pushMessage.message, trigger_username, trigger_char)
            self.__command_handler.handle(userInput, pushMessage, core.bot_controller, core.room_state, core.settings, core.command_controller)

    def __isValidMessage(self, core: Core, pushMessage: PushMessage, trigger_username: str, trigger_char: str = '/') -> bool:
        isUserValid = True
        isMessageValid = True
        # User validation
        if pushMessage.user is None or pushMessage.user.id == core.settings.user_id: 
            isUserValid = False
        # Message validation
        if not ((pushMessage.message.startswith(trigger_char) or pushMessage.message.startswith(trigger_username)) and len(pushMessage.message) > 1):
            isMessageValid = False
        return isUserValid and isMessageValid
        