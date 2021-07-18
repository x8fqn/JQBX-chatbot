import logging, time
import traceback
from src.settings import AbstractSettings, Settings
from src.web_socket_client import AbstractWebSocketClient, WebSocketClient
from src.web_socket_message import WebSocketMessage
from src.web_socket_message_handlers.web_socket_message_handlers import web_socket_message_handler_map

class UnexpectedStop(Exception): 
    pass

class Main():
    def __init__(self, web_socket_client: AbstractWebSocketClient,
    settings: AbstractSettings = Settings.get_instance()) -> None:
        self.ws_client = web_socket_client
        self.settings = settings
        logging.basicConfig(level=self.settings.log_level, format='%(asctime)s - %(module)s -> %(funcName)s - [%(levelname)s] - %(message)s')

    def run(self):
        self.ws_client.register(self.__on_open, self.__on_message, self.__on_error, self.__on_close)
        self.ws_client.run()

    def __on_open(self) -> None:
        logging.info('Websocket connection OPENED')
        self.ws_client.send(WebSocketMessage(label='join', payload={
            'roomId': self.settings.room_id,
            'user': self.settings.user
        }))

    def __on_message(self, message: WebSocketMessage) -> None:
        logging.debug('Incoming Message', message.as_dict())
        try:
            handler = web_socket_message_handler_map.get(message.label, None)
            if handler:
                handler.handle(message)
        except Exception as e:
            logging.error(e)

    def __on_error(self, error: BaseException) -> None:
        logging.error('Error: %s \n Traceback: %s' % (str(error), traceback.format_tb(error.__traceback__)))

    def __on_close(self) -> None:
        logging.info('Websocket connection CLOSED')
        raise UnexpectedStop()


if __name__ == '__main__':
    while True:
        bot = Main(WebSocketClient.get_instance())
        try:
            bot.run()
            logging.warning('Restarting. Send stop signal to exit (5 sec.)')
            time.sleep(5)
        except KeyboardInterrupt:
            logging.warning('Keyboard interrupted, stopping')
            break
        except UnexpectedStop:
            logging.error('Unexpected stop! :(')
    logging.info('Program work is ended!')
