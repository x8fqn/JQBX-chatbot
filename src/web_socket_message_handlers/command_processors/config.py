from src.configuration import Configuration, AbstractConfiguration
from typing import Optional, List

from src.bot_controller import AbstractBotController, BotController
from src.room_state import AbstractRoomState, RoomState
from src.web_socket_message_handlers.command_processors.abstract_command_processor import AbstractCommandProcessor


class ConfigProcessor(AbstractCommandProcessor):
    def __init__(self, room_state: AbstractRoomState = RoomState.get_instance(),
                 bot_controller: AbstractBotController = BotController.get_instance(),
                 config: AbstractConfiguration = Configuration('welcome')):
        self.__room_state = room_state
        self.__bot_controller = bot_controller
        self.__config = config

    @property
    def keyword(self) -> str:
        return 'config'

    @property
    def help(self) -> str:
        return '''
            Bot's components configuration
        '''

    def process(self, user_id: str, payload: Optional[List[str]]) -> None:
        if not self.__isAdmin(user_id): return

        if payload == None:
            self.__bot_controller.chat('Config: welcome')
        args = payload.split(' ', 2)

        if args[0] == 'welcome':
            if 'message' not in self.__config.get().keys():
                self.__bot_controller.chat('No welcome message setted \'/config welcome message {text}\'')
            if 'enabled' not in self.__config.get().keys():
                self.__config.set('enabled', False)

            if len(args) < 2:
                return self.__bot_controller.chat('Config->Welcome: on / off / status / message {text}')
            if args[1] == 'on':
                self.__config.set('enabled', True)
                return self.__bot_controller.chat('Welcome message has been enabled')
            elif args[1] == 'off':
                self.__config.set('enabled', False)
                return self.__bot_controller.chat('Welcome message has been disabled')
            elif args[1] == 'status':
                if self.__config.get()['enabled'] == True:
                    return self.__bot_controller.chat('Welcome text message is ON')
                else:
                    return self.__bot_controller.chat('Welcome text message is OFF')
            elif args[1] == 'message':
                if args[2] != None:
                    self.__config.set('message', args[2])
                    return self.__bot_controller.chat('Message has been successfully changed')
                else:
                    return self.__bot_controller.chat('No message specified')
            else:
                pass
        else:
            self.__bot_controller.chat('Сomponent is not available for configuration')
    
    def __isAdmin(self, user_id: str) -> bool:
        if (user_id in self.__room_state.mod_ids) != True:
            self.__bot_controller.chat('You\'re not moderator or admin')
            return False
        else: return True