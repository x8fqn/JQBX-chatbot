import random
from typing import Optional, List

from src.bot_controller import AbstractBotController, BotController
from src.web_socket_message_handlers.command_processors.abstract_command_processor import AbstractCommandProcessor


class CharlixcxCommandProcessor(AbstractCommandProcessor):
    def __init__(self, bot_controller: AbstractBotController = BotController.get_instance()):
        self.__bot_controller = bot_controller

    @property
    def keyword(self) -> str:
        return 'charlixcx'

    @property
    def help(self) -> str:
        return 'Bring me the pictures of Charli XCX immediately!'

    def process(self, user_id: str, payload: Optional[str]) -> None:
        gifs: List[str] = [
            'https://media2.giphy.com/media/LrGH9gVJF4DEr13oZX/giphy.gif',
            'https://media3.giphy.com/media/gfC7XmjcakaaWcBNiI/giphy.gif',
            'https://media3.giphy.com/media/l3vRgsqe79vhMHeJq/giphy.gif',
            'https://media0.giphy.com/media/SvFFTQE2lD6TWKwV2M/giphy.gif',
            'https://media4.giphy.com/media/Xy7LMINKRKRHNTejqF/giphy.gif',
            'https://media3.giphy.com/media/W6okSyr9D0OmRKDT8R/giphy.gif',
            'https://media0.giphy.com/media/f6skkkRmlX1UItBzML/giphy.gif',
            'https://media4.giphy.com/media/gK6QUfpZzbgaDegFnP/giphy.gif'
        ]
        random.shuffle(gifs)
        self.__bot_controller.chat(random.choice(gifs))
