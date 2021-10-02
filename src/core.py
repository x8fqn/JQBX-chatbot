import spotipy
from src.bot_controller import AbstractBotController, BotController
from src.command_controller import AbstractCommandController, CommandController
from src.room_state import AbstractRoomState, RoomState
from src.settings import AbstractSettings, Settings
from src.web_socket_client import AbstractWebSocketClient, WebSocketClient

class Core:
    def __init__(self) -> None:
        self.settings: AbstractSettings = Settings()
        self.ws_client: AbstractWebSocketClient = WebSocketClient()
        self.bot_controller: AbstractBotController = BotController(self.ws_client, self.settings)
        self.room_state: AbstractRoomState = RoomState(self.bot_controller)
        self.command_controller: AbstractCommandController = CommandController()
        self.spotify = None
        if (self.settings.spotify_refresh_token and self.settings.spotify_client_id and self.settings.spotify_client_secret):
            spotify_auth = spotipy.oauth2.SpotifyOAuth(client_id=self.settings.spotify_client_id,
                client_secret=self.settings.spotify_client_secret, redirect_uri='https://localhost')
            spotify_auth.refresh_access_token(self.settings.spotify_refresh_token)
            self.spotify = spotipy.Spotify(auth_manager=spotify_auth)