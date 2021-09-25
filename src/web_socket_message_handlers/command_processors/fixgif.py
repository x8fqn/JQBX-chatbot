from typing import Optional, List
from src.bot_controller import AbstractBotController, BotController
from src.room_state import AbstractRoomState, RoomState
from src.web_socket_message_handlers.command_processors.abstract_command_processor import AbstractCommandProcessor
from src.web_socket_message_handlers.objects.user_input import UserInput
from src.web_socket_message_handlers.objects.push_message import PushMessage


class FixGifCommandProcessor(AbstractCommandProcessor):
    def __init__(self, room_state: AbstractRoomState = RoomState.get_instance(),
                 bot_controller: AbstractBotController = BotController.get_instance()):
        self.__room_state = room_state
        self.__bot_controller = bot_controller

    @property
    def keyword(self) -> str:
        return 'fixgif'

    @property
    def help(self) -> str:
        return '''
            Fixes the last link to gif 
        '''

    def process(self, pushMessage: PushMessage, userInput: UserInput) -> None:
        isFixed = False
        extensions = ('.gif', '.jpg', '.jpeg', '.png')
        if userInput.text:
            if userInput.text.startswith(('https://', 'http://')) & (not userInput.text.endswith(extensions)):
                    url = userInput.text
                    fixed_link = url + '#.gif'
                    isFixed = True
        else:
            for message in self.__room_state.messages:
                if message.message.startswith(('https://', 'http://')) & (not message.message.endswith(extensions)):
                    url = message.message
                    fixed_link = url + '#.gif'
                    isFixed = True
                    break
        if isFixed:
            self.__bot_controller.chat(fixed_link)
        else:
            self.__bot_controller.info_chat('Can\'t find or fix link. Try /%s {link}' % userInput.keyword)


