import os, sys
from typing import Dict, List

def get_bot_user(username: str, user_id: str, image_url: str, thumbUpImage: str = None,
thumbDownImage: str = None, djImage: str = None) -> dict:
    user = {
        'username': username,
        'id': user_id,
        'uri': 'spotify:user:%s' % user_id,
        'device': 'bot',
        'status': 'active',
        'country': 'US',
        'image': image_url
    }
    if djImage: 
        user.update({'djImage': djImage})
    if thumbUpImage: 
        user.update({'thumbsUpImage': thumbUpImage})
    if thumbDownImage: 
        user.update({'thumbsDownImage': thumbDownImage})
    return user

def get_main_dir() -> str:
    return os.getcwd()

def get_config_path() -> str:
    return os.path.join(os.getcwd(), 'config')