import logging, shlex
from html import unescape
from typing import List, Dict, Optional, Union
from src.settings import AbstractSettings, Settings

from src.web_socket_message_handlers.command_processors.abstract_command_processor import AbstractCommandProcessor
from src.web_socket_message_handlers.command_processors.command_processors import command_processors
from src.web_socket_message_handlers.command_processors.help import HelpCommandProcessor
from src.web_socket_message import WebSocketMessage
from src.web_socket_message_handlers.abstract_web_socket_message_handler import AbstractWebSocketMessageHandler
from src.bot_controller import AbstractBotController, BotController


class PushMessageHandler(AbstractWebSocketMessageHandler):
    def __init__(self, bot_controller: AbstractBotController = BotController.get_instance(),
                 settings: AbstractSettings = Settings.get_instance(),
                 _command_processors: List[AbstractCommandProcessor] = None):
        self.__bot_controller = bot_controller
        self.__settings = settings
        self.__command_processors: Dict[str, AbstractCommandProcessor] = {
            x.keyword: x for x in _command_processors or (command_processors + [HelpCommandProcessor()])
        }

    @property
    def message_label(self) -> str:
        return 'push-message'

    def handle(self, message: WebSocketMessage) -> None:
        payload = message.payload
        message = unescape(payload['message'].strip())
        user_id = self.__getUserID(payload)
        if not self.__isValidUser(user_id): return
        if not self.__isValidMessage(message): return

        message_parts = message.split(' ', 1)
        keyword = message_parts[0].lower().split('/', 1)[-1]
        users_payload = [] if len(message_parts) == 1 else self.__usersPayloadProcess(message_parts[1])

        command_processor = self.__command_processors.get(keyword)
        logging.info('%s called by %s' % (repr(message_parts), (self.__getUsername(payload) or user_id)))
        if command_processor:
            try:
                command_processor.process(user_id, users_payload)
            except IndexError:
                self.__bot_controller.chat('Unable to process input data. Please, specify the request')
            except Exception as e:
                logging.error(e)
                self.__bot_controller.chat('An error occurred while processing the command')

    def __getUserID(self, payload: dict):
        return payload.get('user', {}).get('id', None)

    def __getUsername(self, payload: dict):
        return payload.get('user', {}).get('username')

    def __isValidUser(self, user_id: str) -> bool:
        if user_id is None or user_id == self.__settings.user_id: 
            return False
        else: return True
    
    def __isValidMessage(self, message: str) -> bool:
        if not (message.startswith('/') and len(message) > 1):
            return False
        else: return True

    def __usersPayloadProcess(self, payload: str) -> Optional[List[str]]:
        return shlex.split(payload)
