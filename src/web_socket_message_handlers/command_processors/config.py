from typing import Optional, List

from src.bot_controller import AbstractBotController, BotController
from src.room_state import AbstractRoomState, RoomState
from src.web_socket_message_handlers.command_processors.abstract_command_processor import AbstractCommandProcessor
from src.settings import AbstractSettings, Settings


class ConfigProcessor(AbstractCommandProcessor):
    def __init__(self, room_state: AbstractRoomState = RoomState.get_instance(),
                 bot_controller: AbstractBotController = BotController.get_instance(),
                 settings: AbstractSettings = Settings.get_instance()):
        self.__room_state = room_state
        self.__bot_controller = bot_controller
        self.__settings = settings

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

        if 'bot' in args[0]:
            self.__configure_bot(args[1:])
        elif 'welcome' in args[0]:
            self.__configure_welcome(args[1:])
        else:
            self.__bot_controller.chat('Сomponent is not available for configuration')


    def __isAdmin(self, user_id: str) -> bool:
        if (user_id in self.__room_state.mod_ids) != True:
            self.__bot_controller.chat('You\'re not moderator or admin')
            return False
        else: return True

    def __noArguments(self, payload) -> bool:
        if payload == []:
            self.__bot_controller.chat('Possible options: bot / welcome')
            return True
        else: 
            return False

    def __configure_bot(self, args: List[Optional[str]]) -> None:
        if 'name' in args[0]:
            new_name, old_name = ' '.join(args[1:]), self.__settings.user['username']
            self.__settings.set_username(new_name)
            self.__bot_controller.update_user()
            self.__bot_controller.chat('Changed bot username: "%s" -> "%s"' % (old_name, new_name))
        elif 'image' in args[0]:
            if 'dj' in args[1]: 
                self.__bot_controller.chat('Bot previous "DJ" image: %s' % self.__settings.user['djImage'])
                self.__settings.set_image(3, args[2])
                self.__bot_controller.update_user()
            elif ('up' or 'thumbUp') in args[1]:
                self.__bot_controller.chat('Bot previous "thumbUp" image: %s' % self.__settings.user['thumbsUpImage'])
                self.__settings.set_image(1, args[2])
                self.__bot_controller.update_user()
            elif ('down' or 'thumbDown') in args[1]:
                self.__bot_controller.chat('Bot previous "thumbDown" image: %s' % self.__settings.user['thumbsDownImage'])
                self.__settings.set_image(2, args[2])
                self.__bot_controller.update_user()
            else: 
                self.__bot_controller.chat('Bot previous main image: %s' % self.__settings.user['image'])
                self.__settings.set_image(0, args[1])
                self.__bot_controller.update_user()

    def __configure_welcome(self, args: Optional[List[str]]) -> None:
        if 'on' in args[0]:
            self.__settings.welcome_set_enable(True)
            self.__bot_controller.chat('Welcome message has been enabled')
        elif 'off' in args[0]:
            self.__settings.welcome_set_enable(False)
            self.__bot_controller.chat('Welcome message has been disabled')
        elif 'status' in args[0]:
            msg = 'Status: ' + ('enabled' if self.__settings.welcome_isEnabled else 'disabled') + '; '
            msg += 'Whisper: ' + ('yes' if self.__settings.welcome_isWhisper else 'no') + '; '
            msg += 'Message: '
            self.__bot_controller.chat(msg)
            self.__bot_controller.chat('"' + self.__settings.welcome_message + '"')
        elif 'message' in args[0]:
            self.__settings.welcome_set_message(' '.join(args[1:]))
            self.__bot_controller.chat('Message has been successfully changed')
        elif 'whisper' in args[0]:
            if 'on' in args[1]:
                self.__settings.welcome_set_whisper(True)
                self.__bot_controller.chat('Welcome whisper mode has been enabled')
            elif 'off' in args[1]:
                self.__bot_controller.chat('Welcome whisper mode has been disabled')
                self.__settings.welcome_set_whisper(False)
        else:
            self.__bot_controller.chat('Possible options of welcome: on / off / status / message "{text}"')