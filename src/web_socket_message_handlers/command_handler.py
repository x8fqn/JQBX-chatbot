    
from typing import Union
from src.settings import AbstractSettings
from src.room_state import AbstractRoomState
from src.bot_controller import AbstractBotController, BotController
from src.command_controller import AbstractCommandController, CommandController
from src.db_controllers.custom_commands import Alias, Single
from src.web_socket_message_handlers.command_processors.command_processors import Processors
from src.web_socket_message_handlers.objects.push_message import PushMessage
from src.web_socket_message_handlers.objects.user_input import UserInput
from src.web_socket_message_handlers.command_processors.help import HelpCommandProcessor
from datetime import datetime
from src.jqbx_api import JQBXAPI


class CommandHandler:
    def __init__(self
    # bot_controller: AbstractBotController = BotController.get_instance(),
    # command_comtroller: AbstractCommandController = CommandController.get_instance()
    ) -> None:
        # self.__bot_controller = bot_controller
        # self.__command_controller = command_comtroller
        self.__processors = Processors()


    def handle(self, userInput: UserInput, pushMessage_obj: PushMessage, 
    bot_controller: AbstractBotController, room_state: AbstractRoomState, settings: AbstractSettings, command_controller: AbstractCommandController):
        if userInput.keyword in self.__processors.command_processors:
            self.__processors.get(userInput.keyword).process(pushMessage_obj, userInput, bot_controller, room_state, settings, command_controller)
        elif userInput.keyword in 'help':
            HelpCommandProcessor().process(pushMessage_obj, userInput, bot_controller, room_state, settings, command_controller)
        else:
            command = command_controller.get_command(userInput.keyword)
            if command:
                self.__preprocess(pushMessage_obj, userInput, command, bot_controller, room_state, settings, command_controller)

    def __preprocess(self, pushMessage: PushMessage, userInput: UserInput, command: Union[Single, Alias], 
    bot_controller: AbstractBotController, room_state: AbstractRoomState, settings: AbstractSettings, command_controller: AbstractCommandController):
        if userInput.args_check('remove', 0):
            if command_controller.remove_command(command):
                bot_controller.info_chat('Done!')
            else:
                bot_controller.info_chat('Failed!')
        elif userInput.args_check('info', 0):
            msg = []
            types = ['Single', 'Collection', 'Alias', 'Action']
            msg.append('Name - %s, ID - %s, Type - %s' % (command.name, str(command.command_id), types[command.type]))
            msg.append('Added by %s at %s' % (
                JQBXAPI.user('spotify:user:' + command.publisher_id).primaryUsername(),
                datetime.fromtimestamp(command.added_timestamp).strftime('%m/%d/%Y')
            ))
            bot_controller.chat(msg)
        else: 
            self.__command_process(command, pushMessage, userInput, bot_controller, room_state, settings, command_controller)

    def __command_process(self, command: Union[Single, Alias], pushMessage: PushMessage, userInput: UserInput, 
    bot_controller: AbstractBotController, room_state: AbstractRoomState, settings: AbstractSettings, command_controller: AbstractCommandController):
        if isinstance(command, Single):
            bot_controller.chat(command.message)
        elif isinstance(command, Alias):
            self.__alias_process(command, pushMessage, userInput, bot_controller, room_state, settings, command_controller)
        
    def __alias_process(self, command: Alias, pushMessage: PushMessage, userInput: UserInput, 
    bot_controller: AbstractBotController, room_state: AbstractRoomState, settings: AbstractSettings, command_controller: AbstractCommandController):
        if command.keyword in self.__processors.command_processors:
            self.__processors.get(command.keyword).process(pushMessage, userInput, bot_controller, room_state, settings, command_controller)
        else:
            command = command_controller.get_command(command.keyword)
            if command:
                self.__command_process(command, pushMessage, userInput, bot_controller, room_state, settings, command_controller)   