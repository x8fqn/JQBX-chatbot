import logging, time
from src.web_socket_message import WebSocketMessage
from src.web_socket_message_handlers.web_socket_message_handlers import web_socket_message_handler_map
from src.web_socket_message_handlers.abstract_web_socket_message_handler import AbstractWebSocketMessageHandler
from src.core import Core

class UnexpectedStop(Exception): 
    pass


class Main():
    def __init__(self) -> None:
        self.core = Core()
        logging.basicConfig(level=self.core.settings.log_level, format='%(asctime)s - %(module)s -> %(funcName)s - [%(levelname)s] - %(message)s')

    def run(self):
        self.core.ws_client.register(self.__on_open, self.__on_message, self.__on_error, self.__on_close)
        self.core.ws_client.run()

    def __on_open(self) -> None:
        logging.info('Websocket connection OPENED')
        self.core.ws_client.send(WebSocketMessage(label='join', payload={
            'roomId': self.core.settings.room_id,
            'user': self.core.settings.user
        }))

    def __on_message(self, message: WebSocketMessage) -> None:
        logging.debug('Incoming Message', message.as_dict())
        try:
            handler: AbstractWebSocketMessageHandler = web_socket_message_handler_map.get(message.label, None)
            if handler:
                handler.handle(message, self.core)
        except Exception as e:
            logging.error(e)

    def __on_error(self, error: BaseException) -> None:
        if isinstance(error, KeyboardInterrupt):
            logging.error('Keyboard interrupted!')
        else:
            logging.error(error)

    def __on_close(self) -> None:
        logging.info('Websocket connection CLOSED')
        raise UnexpectedStop()


if __name__ == '__main__':
    while True:
        bot = Main()
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
