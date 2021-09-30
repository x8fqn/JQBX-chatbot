from typing import Optional, List

from src.web_socket_message_handlers.command_processors.abstract_command_processor import AbstractCommandProcessor
from src.web_socket_message_handlers.objects.user_input import UserInput
from src.web_socket_message_handlers.objects.push_message import PushMessage
from src.command_controller import AbstractCommandController
from src.bot_controller import AbstractBotController
from src.command_controller import AbstractCommandController
from src.room_state import AbstractRoomState
from src.settings import AbstractSettings

class ConfigProcessor(AbstractCommandProcessor):
    @property
    def keyword(self) -> str:
        return 'config'

    @property
    def help(self) -> str:
        return '''
            Bot's components configurator
        '''

    def process(self, pushMessage: PushMessage, userInput: UserInput,
    bot_controller: AbstractBotController, room_state: AbstractRoomState, settings: AbstractSettings, command_controller: AbstractCommandController) -> None:
        if not self.__isAdmin(pushMessage.user.id, bot_controller, room_state): return
        if self.__noArguments(userInput.arguments, bot_controller): return

        if userInput.args_check('bot', 0):
            self.__configure_bot(userInput.arguments[1:], bot_controller, settings, room_state)
        elif userInput.args_check('welcome', 0):
            self.__configure_welcome(userInput.arguments[1:], bot_controller, settings)
        else:
            bot_controller.chat('Сomponent is not available for configuration')


    def __isAdmin(self, user_id: str, bot_controller: AbstractBotController, room_state: AbstractRoomState) -> bool:
        if (user_id in room_state.mod_ids) != True:
            bot_controller.chat('You\'re not moderator or admin')
            return False
        else: return True

    def __noArguments(self, payload, bot_controller: AbstractBotController) -> bool:
        if payload == None:
            bot_controller.chat('Possible options: bot / welcome')
            return True
        else: 
            return False

    def __configure_bot(self, args: List[Optional[str]], bot_controller: AbstractBotController, settings: AbstractSettings, room_state: AbstractRoomState) -> None:
        if 'name' in args[0]:
            new_name, old_name = ' '.join(args[1:]), settings.user.get('username', 'None')
            settings.set_username(new_name)
            bot_controller.update_user()
            bot_controller.chat('Changed bot username: "%s" -> "%s"' % (old_name, new_name))
        elif 'image' in args[0]:
            if args[1].startswith(('http://', 'https://')):
                bot_controller.chat('Bot previous main image: %s' % settings.user.get('image', 'None'))
                settings.set_image(0, args[1])
                bot_controller.update_user()
            elif 'dj' in args[1]: 
                bot_controller.chat('Bot previous "DJ" image: %s' % settings.user.get('djImage', 'None'))
                settings.set_image(3, args[2])
                bot_controller.update_user()
            elif ('up' or 'thumbUp') in args[1]:
                bot_controller.chat('Bot previous "thumbUp" image: %s' % settings.user.get('thumbsUpImage', 'None'))
                settings.set_image(1, args[2])
                bot_controller.update_user()
            elif ('down' or 'thumbDown') in args[1]:
                bot_controller.chat('Bot previous "thumbDown" image: %s' % settings.user.get('thumbsDownImage', 'None'))
                settings.set_image(2, args[2])
                bot_controller.update_user()
            else: 
                pass
        else:
            bot_controller.chat('Possible options of bot: name / image {up/down/dj} / image {url}')

    def __configure_welcome(self, args: Optional[List[str]], bot_controller: AbstractBotController, settings: AbstractSettings) -> None:
        if 'on' in args[0]:
            settings.welcome_set_enable(True)
            bot_controller.chat('Welcome message has been enabled')
        elif 'off' in args[0]:
            settings.welcome_set_enable(False)
            bot_controller.chat('Welcome message has been disabled')
        elif 'status' in args[0]:
            msg = 'Status: ' + ('enabled' if settings.welcome_isEnabled else 'disabled') + '; '
            msg += 'Whisper: ' + ('yes' if settings.welcome_isWhisper else 'no') + '; '
            msg += 'Message: '
            bot_controller.chat(msg)
            bot_controller.chat('"' + settings.welcome_message + '"')
        elif 'message' in args[0]:
            settings.welcome_set_message(' '.join(args[1:]))
            bot_controller.chat('Message has been successfully changed')
        elif 'whisper' in args[0]:
            if 'on' in args[1]:
                settings.welcome_set_whisper(True)
                bot_controller.chat('Welcome whisper mode has been enabled')
            elif 'off' in args[1]:
                bot_controller.chat('Welcome whisper mode has been disabled')
                settings.welcome_set_whisper(False)
        else:
            bot_controller.chat('Possible options of welcome: on / off / status / message "{text}"')