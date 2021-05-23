import time
from src.configuration import Configuration, AbstractConfiguration
from src.helpers import get_bot_user
from src.logger import AbstractLogger, Logger
from src.web_socket_client import AbstractWebSocketClient, WebSocketClient
from src.web_socket_message import WebSocketMessage
from src.web_socket_message_handlers.web_socket_message_handlers import web_socket_message_handler_map


def main(web_socket_client: AbstractWebSocketClient, logger: AbstractLogger):
    baseKeysReq = ('spotify_user_id', 'jqbx_room_id', 'jqbx_bot_display_name', 
        'jqbx_bot_image_url', 'log_level')
    config: AbstractConfiguration = Configuration('bot_main', 'config', baseKeysReq)

    def __on_open() -> None:
        logger.info('Websocket connection OPENED')
        web_socket_client.send(WebSocketMessage(label='join', payload={
            'roomId': config.get()['jqbx_room_id'] ,
            'user': get_bot_user(config.get())
        }))

    def __on_message(message: WebSocketMessage) -> None:
        logger.debug('Incoming Message', message.as_dict())
        try:
            handler = web_socket_message_handler_map.get(message.label, None)
            if handler:
                handler.handle(message)
        except Exception as e:
            logger.error(e)

    def __on_error(error: BaseException) -> None:
        logger.error(error)

    def __on_close() -> None:
        logger.info('Websocket connection CLOSED')

    while True:
        web_socket_client.register(__on_open, __on_message, __on_error, __on_close)
        was_keyboard_interrupt = not web_socket_client.run()
        if was_keyboard_interrupt:
            break
        logger.error(Exception('Websocket client stopped. Restarting.'))


if __name__ == '__main__':
    while True:
        main(WebSocketClient.get_instance(), Logger())
        try:
            print('[ALERT] Restarting. Send again to exit (5 sec.)')
            time.sleep(5)
        except KeyboardInterrupt:
            print('[ALERT] Keyboard interrupted, stopping')
            break
print('[INFO] Program work is ended!')
