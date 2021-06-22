from typing import Optional, Dict, List

from bot_controller import AbstractBotController, BotController
from web_socket_message_handlers.command_processors.abstract_command_processor import AbstractCommandProcessor
from web_socket_message_handlers.command_processors.command_processors import command_processors


class HelpCommandProcessor(AbstractCommandProcessor):
    def __init__(self, bot_controller: AbstractBotController = BotController.get_instance()):
        self.__commands: Dict[str, AbstractCommandProcessor] = {
            x.keyword: x for x in command_processors
        }
        self.__bot_controller = bot_controller

    @property
    def keyword(self) -> str:
        return 'help'

    @property
    def help(self) -> str:
        return 'This'

    def process(self, user_id: str, payload: Optional[str]) -> None:
        lines: List[str] = []
        if payload in {None, ''}:
            return self.__bot_controller.chat(
                ', '.join(['/%s' % self.__commands[key].keyword for key in sorted(self.__commands.keys())]))
        payload = payload.strip()
        if payload.startswith(('-', '--')):
            if payload in {'-h', '--help'}:
                helpMsg = [
                'Usage:',
                '/help [command] - get a command description',
                '/help --verbose',
                'Arguments:',
                '--help - show this message',
                '-v, --verbose - informative version of help (for desktop)']
                return self.__bot_controller.chat(helpMsg)
            elif payload in {'-v', '--verbose'}:
                return self.__bot_controller.chat(
                    ['/%s - %s' % (self.__commands[key].keyword, self.__commands[key].help) for key in sorted(self.__commands.keys())])
        if payload in [self.__commands[key].keyword for key in self.__commands.keys()]:
            for key in self.__commands.keys():
                if self.__commands[key].keyword == payload:
                    return self.__bot_controller.chat('/%s - %s' % (self.__commands[key].keyword, self.__commands[key].help))

