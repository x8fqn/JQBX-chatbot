from src.modules.youtube import Youtube
from src.web_socket_message_handlers.command_processors.abstract_command_processor import AbstractCommandProcessor
from src.web_socket_message_handlers.objects.user_input import UserInput
from src.web_socket_message_handlers.objects.push_message import PushMessage
from src.command_controller import AbstractCommandController
from src.bot_controller import AbstractBotController
from src.command_controller import AbstractCommandController
from src.room_state import AbstractRoomState
from src.settings import AbstractSettings


class YtCommandProcessor(AbstractCommandProcessor):
    @property
    def keyword(self) -> str:
        return 'yt'

    @property
    def help(self) -> str:
        return '''
            Find the link to this tune on YouTube
        '''

    def process(self, pushMessage: PushMessage, userInput: UserInput,
    bot_controller: AbstractBotController, room_state: AbstractRoomState, settings: AbstractSettings, command_controller: AbstractCommandController) -> None:
        result = Youtube.searchTune(room_state.current_track['name'], 
            [artist['name'] for artist in room_state.current_track['artists']],
            room_state.current_track['duration_ms'] // 1000)
        if result != False:
            bot_controller.chat('%s#.jpg %s' % (result['thumbnail'], result['url']))
        else:
            bot_controller.chat('Couldn\'t find this on YouTube')
