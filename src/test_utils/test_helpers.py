import random
import string


def create_random_string(size: int = 10) -> str:
    return ''.join(str(random.choice(string.ascii_letters)) for _ in range(size))


def create_random_id_object() -> dict:
    return {'id': create_random_string()}

def create_random_track_object(track_id: str = create_random_string(),
user_id: str = create_random_string(), started_at: float = random.randrange(100, 10000000),
artist: str = create_random_string(3), track_name: str = create_random_string(5)) -> dict:
    return {
         "id": track_id,
         "href": "https://api.spotify.com/v1/tracks/%s" % track_id,
         "name": track_name,
         "artists": artist,
         "uri": "spotify:track:%s" % track_id,
         "userUri": "spotify:user:%s" % user_id,
         "username": user_id,
         "startedAt": started_at
      }
