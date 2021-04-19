from typing import Optional

from dependency_injector.wiring import inject

from src.bot_controller import AbstractBotController, BotController
from src.web_socket_message_handlers.command_processors.abstract_command_processor import AbstractCommandProcessor
from src.room_state import AbstractRoomState, RoomState


class WelcomeCommandProcessor(AbstractCommandProcessor):
    @inject
    def __init__(self, bot_controller: AbstractBotController = BotController.get_instance(),
                 room_state: AbstractRoomState = RoomState.get_instance()):
        self.__bot_controller = bot_controller
        self.__room_state = room_state

    @property
    def keyword(self) -> str:
        return 'welcome'

    @property
    def help(self) -> str:
        return '''
            Set a welcome message (or just display the current message if new message not provided)
        '''

    def process(self, user_id: str, payload: Optional[str] = None) -> None:
        is_mod = user_id in self.__room_state.mod_ids
        if not payload:
            if self.__bot_controller.welcome_message:
                self.__bot_controller.chat('The current welcome message is: "%s"' % self.__bot_controller.welcome_message)
            else:
                message = 'The welcome message is not currently set.'
                if is_mod:
                    message += ' To set one, type `/welcome [message]`.'
                self.__bot_controller.chat(message)
            return
        if not is_mod:
            self.__bot_controller.chat('Only mods can update the welcome message!')
            return
        self.__bot_controller.set_welcome_message(payload)
        self.__bot_controller.chat('The welcome message has been set to: "%s"' % payload)
