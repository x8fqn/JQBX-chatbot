from src.web_socket_message_handlers.command_processors.abstract_command_processor import AbstractCommandProcessor
from src.web_socket_message_handlers.objects.user_input import UserInput
from src.web_socket_message_handlers.objects.push_message import PushMessage
from src.command_controller import AbstractCommandController
from src.bot_controller import AbstractBotController
from src.command_controller import AbstractCommandController
from src.room_state import AbstractRoomState
from src.settings import AbstractSettings

class FixGifCommandProcessor(AbstractCommandProcessor):
    @property
    def keyword(self) -> str:
        return 'fixgif'

    @property
    def help(self) -> str:
        return '''
            Fixes the last link to gif 
        '''

    def process(self, pushMessage: PushMessage, userInput: UserInput,
    bot_controller: AbstractBotController, room_state: AbstractRoomState, settings: AbstractSettings, command_controller: AbstractCommandController) -> None:
        isFixed = False
        extensions = ('.gif', '.jpg', '.jpeg', '.png')
        if userInput.text:
            if userInput.text.startswith(('https://', 'http://')) & (not userInput.text.endswith(extensions)):
                    url = userInput.text
                    fixed_link = url + '#.gif'
                    isFixed = True
        else:
            for message in room_state.messages:
                if message.message.startswith(('https://', 'http://')) & (not message.message.endswith(extensions)):
                    url = message.message
                    fixed_link = url + '#.gif'
                    isFixed = True
                    break
        if isFixed:
            bot_controller.chat(fixed_link)
        else:
            bot_controller.info_chat('Can\'t find or fix link. Try /%s {link}' % userInput.keyword)


