from typing import Optional, List

from src.bot_controller import AbstractBotController, BotController
from src.room_state import AbstractRoomState, RoomState
from src.web_socket_message_handlers.command_processors.abstract_command_processor import AbstractCommandProcessor
from src.web_socket_message_handlers.command_processors.workers.configure import Configure


class ConfigProcessor(AbstractCommandProcessor):
    def __init__(self, room_state: AbstractRoomState = RoomState.get_instance(),
                 bot_controller: AbstractBotController = BotController.get_instance()):
        self.__room_state = room_state
        self.__bot_controller = bot_controller
        self.__configurator = Configure(self.__bot_controller)

    @property
    def keyword(self) -> str:
        return 'config'

    @property
    def help(self) -> str:
        return '''
            Bot's components configurator
        '''

    def process(self, user_id: str, args: Optional[List[str]]) -> None:
        if not self.__isAdmin(user_id): return
        if self.__noArguments(args): return

        try:
            if 'welcome' in args[0]:
                self.__configure_welcome(args[1:])
            else:
                self.__bot_controller.chat('Сomponent is not available for configuration')
        except IndexError:
            # self.__bot_controller.chat('Please, make sure you entered the query correctly')
            self.__bot_controller.chat('Possible options of welcome: on / off / status / message "{text}"')

    def __isAdmin(self, user_id: str) -> bool:
        if (user_id in self.__room_state.mod_ids) != True:
            self.__bot_controller.chat('You\'re not moderator or admin')
            return False
        else: return True

    def __noArguments(self, payload) -> bool:
        if payload == None:
            self.__bot_controller.chat('Config: welcome')
            return True
        else: 
            return False

    def __configure_welcome(self, args: Optional[List[str]]) -> None:
            if 'on' in args[0]:
                self.__configurator.welcome_enable(True)
                self.__bot_controller.chat('Welcome message has been enabled')
            elif 'off' in args[0]:
                self.__configurator.welcome_enable(False)
                self.__bot_controller.chat('Welcome message has been disabled')
            elif 'status' in args[0]:
                msg = 'Status: ' + ('enabled' if self.__bot_controller.welcome_isEnabled else 'disabled') + '; '
                msg += 'Whisper: ' + ('yes' if self.__bot_controller.welcome_isWhisper else 'no') + '; '
                msg += 'Message: '
                self.__bot_controller.chat(msg)
                self.__bot_controller.chat('"' + self.__configurator.welcome_message + '"')
            elif 'message' in args[0]:
                self.__configurator.welcome_set_meessage(' '.join(args[1:]))
                self.__bot_controller.chat('Message has been successfully changed')
            elif 'whisper' in args[0]:
                if 'on' in args[1]:
                    self.__configurator.welcome_whisper(True)
                    self.__bot_controller.chat('Welcome whisper mode has been enabled')
                elif 'off' in args[1]:
                    self.__bot_controller.chat('Welcome whisper mode has been disabled')
                    self.__configurator.welcome_whisper(False)

            else:
                self.__bot_controller.chat('Possible options of welcome: on / off / status / message "{text}"')