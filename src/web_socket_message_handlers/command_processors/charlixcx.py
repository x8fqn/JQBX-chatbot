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
            'https://media4.giphy.com/media/gK6QUfpZzbgaDegFnP/giphy.gif',
            'https://media3.giphy.com/media/iH29zOShq2xmoqvYgf/giphy.gif',
            'https://media3.giphy.com/media/RhN0KtlPERCOy5n8S1/giphy.gif',
            'https://media2.giphy.com/media/Wt0ThupWkMnGFng4fl/giphy.gif',
            'https://media3.giphy.com/media/5h5zAh85EEAIfjo926/giphy.gif',
            'https://media4.giphy.com/media/KH3JkhMhCMdt9G7O9Z/giphy.gif',
            'https://media1.giphy.com/media/Q8lTHW7pGq3eoWi35I/giphy.gif',
            'https://media4.giphy.com/media/RGdtnD2LNFrVM4Zv5N/giphy.gif',
            'https://media2.giphy.com/media/TIR9f2CfySlFplAoSA/giphy.gif',
            'https://media1.giphy.com/media/zf0ZBORj3ukDu/giphy.gif'
        ]
        random.shuffle(gifs)
        self.__bot_controller.chat(random.choice(gifs))
