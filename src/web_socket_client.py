import logging, json, re
from abc import ABC, abstractmethod
from typing import Callable, Optional, Any
from websocket import WebSocketApp
from src.web_socket_message import WebSocketMessage


class AbstractWebSocketClient(ABC):
    @abstractmethod
    def register(self, on_open: Callable[[], None], on_message: Callable[[WebSocketMessage], None],
                 on_error: Callable[[Any], None], on_close: Callable[[], None]) -> None:
        pass

    @abstractmethod
    def run(self) -> None:
        pass

    @abstractmethod
    def send(self, web_socket_message: WebSocketMessage) -> None:
        pass


class WebSocketClient(AbstractWebSocketClient):
    __instance: Optional['WebSocketClient'] = None

    def __init__(self):
        # if WebSocketClient.__instance:
        #     raise Exception('Use get_instance() instead!')
        self.__ws = WebSocketApp('wss://jqbx.fm/socket.io/?EIO=3&transport=websocket')
        WebSocketClient.__instance = self

    @staticmethod
    def get_instance() -> 'WebSocketClient':
        if WebSocketClient.__instance is None:
            WebSocketClient()
        return WebSocketClient.__instance

    def register(self, on_open: Callable[[], None], on_message: Callable[[WebSocketMessage], None],
                 on_error: Callable[[Any], None], on_close: Callable[[], None]) -> None:
        self.__ws.on_open = lambda _: on_open()
        self.__ws.on_message = lambda _, raw_message: on_message(self.__parse(raw_message))
        self.__ws.on_error = lambda _, error: on_error(error)
        self.__ws.on_close = lambda _: on_close()

    def run(self) -> None:
        self.__ws.run_forever()

    def send(self, web_socket_message: WebSocketMessage) -> None:
        logging.debug('Outgoing Message: %s' % repr(web_socket_message.as_dict()))
        serialized = str(web_socket_message.code)
        array_part = [x for x in [web_socket_message.label, web_socket_message.payload] if x]
        if array_part:
            serialized += json.dumps(array_part)
        self.__ws.send(serialized)

    @staticmethod
    def __parse(raw_message: str) -> WebSocketMessage:
        parsing = [match for match in enumerate(re.finditer(r'(\d+)(.*)', raw_message))][0][1].groups()
        code = int(parsing[0])
        payload = json.loads(parsing[1]) if parsing[1] != '' else None
        if isinstance(payload, list):
            label = payload[0]
            if len(payload) > 1:
                payload = payload[1]
            else:
                payload = None
        else:
            label = None
        return WebSocketMessage(code, label, payload)
