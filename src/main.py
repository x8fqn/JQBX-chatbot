import logging, time
import traceback
from configuration import Configuration, AbstractConfiguration
from helpers import get_bot_user
from web_socket_client import AbstractWebSocketClient, WebSocketClient
from web_socket_message import WebSocketMessage
from web_socket_message_handlers.web_socket_message_handlers import web_socket_message_handler_map


def main(web_socket_client: AbstractWebSocketClient):
    baseKeysReq = ('spotify_user_id', 'jqbx_room_id', 'jqbx_bot_display_name', 
        'jqbx_bot_image_url', 'log_level')
    config: AbstractConfiguration = Configuration('bot_main', '../config', baseKeysReq)
    logging.basicConfig(level=config.get()['log_level'], format='%(asctime)s - %(module)s -> %(funcName)s - [%(levelname)s] - %(message)s')
    def __on_open() -> None:
        logging.info('Websocket connection OPENED')
        web_socket_client.send(WebSocketMessage(label='join', payload={
            'roomId': config.get()['jqbx_room_id'] ,
            'user': get_bot_user(config.get())
        }))

    def __on_message(message: WebSocketMessage) -> None:
        logging.debug('Incoming Message', message.as_dict())
        try:
            handler = web_socket_message_handler_map.get(message.label, None)
            if handler:
                handler.handle(message)
        except Exception as e:
            logging.error(e)

    def __on_error(error: BaseException) -> None:
        logging.error('Error: %s \n Traceback: %s' % (str(error), traceback.format_tb(error.__traceback__)))

    def __on_close() -> None:
        logging.info('Websocket connection CLOSED')

    while True:
        web_socket_client.register(__on_open, __on_message, __on_error, __on_close)
        was_keyboard_interrupt = not web_socket_client.run()
        if was_keyboard_interrupt:
            break
        logging.error(Exception('Websocket client stopped. Restarting.'))


if __name__ == '__main__':
    while True:
        main(WebSocketClient.get_instance())
        try:
            logging.warning('Restarting. Send again to exit (5 sec.)')
            time.sleep(5)
        except KeyboardInterrupt:
            logging.warning('Keyboard interrupted, stopping')
            break
    logging.info('Program work is ended!')
