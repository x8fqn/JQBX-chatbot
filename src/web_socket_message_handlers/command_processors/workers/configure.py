from src.bot_controller import AbstractBotController

class Configure:
    def __init__(self, bot_controller: AbstractBotController) -> None:
        self.__bot_controller = bot_controller

    def welcome_set_meessage(self, msg: str) -> None:
        self.__bot_controller.welcome_set_message(msg)

    def welcome_enable(self, enable: bool) -> None:
        self.__bot_controller.welcome_set_enable(enable)

    def welcome_whisper(self, enable: bool) -> None:
        self.__bot_controller.welcome_set_whisper(enable)

    @property
    def welcome_isEnabled(self) -> bool:
        return self.__bot_controller.welcome_isEnabled

    @property
    def welcome_message(self) -> str:
        return self.__bot_controller.welcome_message

    @property
    def welcome_isWhisper(self) -> str:
        return self.__bot_controller.welcome_isWhisper
