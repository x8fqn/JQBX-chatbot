def get_bot_user(config: dict) -> dict:
    return {
        'username': config['jqbx_bot_display_name'],
        'id': config['spotify_user_id'],
        'uri': 'spotify:user:%s' % config['spotify_user_id'],
        'device': 'bot',
        'status': 'active',
        'country': 'US',
        'image': config['jqbx_bot_image_url']
    }
